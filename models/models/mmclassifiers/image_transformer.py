# Copyright (c) OpenMMLab. All rights reserved.

import numpy as np
import torch
from mmcls.models import VisionTransformer
from mmcls.models.backbones.vision_transformer import TransformerEncoderLayer
from mmcv.cnn import build_norm_layer
from mmcv.runner import BaseModule
from torch import nn
from torch.nn import ModuleList

from .image import ImageClassifier


class TransformerLayers(VisionTransformer):
    def __init__(self,
                 arch = 'base',
                 embed_dims = None,
                 num_layers = None,
                 num_patches = 16,
                 drop_rate = 0.,
                 drop_path_rate = 0.,
                 qkv_bias = True,
                 norm_cfg = dict(type = 'LN', eps = 1e-6),
                 final_norm = True,
                 with_cls_token = True,
                 layer_cfgs = dict(),
                 init_cfg = None):
        super(VisionTransformer, self).__init__(init_cfg)

        if isinstance(arch, str):
            arch = arch.lower()
            assert arch in set(self.arch_zoo), \
                f'Arch {arch} is not in default archs {set(self.arch_zoo)}'
            self.arch_settings = self.arch_zoo[arch]
        else:
            essential_keys = {
                'embed_dims', 'num_layers', 'num_heads', 'feedforward_channels'
            }
            assert isinstance(arch, dict) and essential_keys <= set(arch), \
                f'Custom arch needs a dict with keys {essential_keys}'
            self.arch_settings = arch

        self.embed_dims = embed_dims or self.arch_settings['embed_dims']
        self.num_layers = num_layers or self.arch_settings['num_layers']

        # Set cls token
        self.with_cls_token = with_cls_token
        self.cls_token = nn.Parameter(torch.zeros(1, 1, self.embed_dims))

        # Set position embedding
        self.pos_embed = nn.Parameter(torch.zeros(1, num_patches + self.num_extra_tokens, self.embed_dims))
        self._register_load_state_dict_pre_hook(self._prepare_pos_embed)

        self.drop_after_pos = nn.Dropout(p = drop_rate)

        # stochastic depth decay rule
        dpr = np.linspace(0, drop_path_rate, self.num_layers)

        self.layers = ModuleList()
        if isinstance(layer_cfgs, dict):
            layer_cfgs = [layer_cfgs] * self.num_layers
        for i in range(self.num_layers):
            _layer_cfg = dict(
                embed_dims = self.embed_dims,
                num_heads = self.arch_settings['num_heads'],
                feedforward_channels = self.arch_settings['feedforward_channels'],
                drop_rate = drop_rate,
                drop_path_rate = dpr[i],
                qkv_bias = qkv_bias,
                norm_cfg = norm_cfg)
            _layer_cfg.update(layer_cfgs[i])
            self.layers.append(TransformerEncoderLayer(**_layer_cfg))

        self.final_norm = final_norm
        if final_norm:
            self.norm1_name, norm1 = build_norm_layer(
                norm_cfg, self.embed_dims, postfix = 1)
            self.add_module(self.norm1_name, norm1)

    @property
    def norm1(self):
        return getattr(self, self.norm1_name)

    def embed_forward(self, x):
        # stole cls_tokens impl from Phil Wang, thanks
        cls_tokens = self.cls_token.expand(x.shape[0], -1, -1)
        x = torch.cat((cls_tokens, x), dim = 1)
        x = x + self.pos_embed
        x = self.drop_after_pos(x)
        return x

    def forward(self, x, stage = None):
        if not self.with_cls_token:
            # Remove class token for transformer encoder input
            x = x[:, 1:]

        layer = self.layers[stage]
        x = layer(x)

        if stage == len(self.layers) - 1 and self.final_norm:
            x = self.norm1(x)

        return x


class FusionTransformer(BaseModule):
    def __init__(self, transformer_cfg, num_transformer, out_indices = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        assert num_transformer > 0, 'FusionTransformer except more than zero transformer'

        self.num_transformer = num_transformer
        self.transformer_cfg = transformer_cfg
        self.out_indices = out_indices
        self.transformers = nn.ModuleList([TransformerLayers(**transformer_cfg) for _ in range(num_transformer)])
        self.num_layers = self.transformers[0].num_layers
        self.with_cls_token = self.transformers[0].with_cls_token

    def embed_forward(self, feats):
        return [transformer.embed_forward(feat) for feat, transformer in zip(feats, self.transformers)]

    def forward(self, feats):
        assert len(feats) == self.num_transformer, 'FusionTransformer only accept same transformer number'
        out_feats = []
        for stage in range(self.num_layers):
            feats = [transformer(feat, stage = stage) for feat, transformer in zip(feats, self.transformers)]

            if self.out_indices is None or stage in self.out_indices:
                out_feats.append(feats)

            fusion_token = torch.mean(torch.stack([f[:, -1] for f in feats], dim = 1), dim = 1, keepdim = True)
            feats = [torch.cat([f[:, :-1], fusion_token], dim = 1) for f in feats]

        return out_feats


class ImageTransformerClassifier(ImageClassifier):
    def __init__(self,
                 center_size = 1,
                 in_channels = 512,
                 num_img_token = 4,
                 fusion_transformer_cfg = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fusion_transformer_cfg = fusion_transformer_cfg
        self.fusion_transformer = FusionTransformer(**fusion_transformer_cfg)
        self.embed_dims = self.fusion_transformer.transformers[0].embed_dims
        self.num_transformer = self.fusion_transformer.num_transformer
        assert self.num_transformer in [1, 2], 'ImageTransformerWithLabelClassifier only support one or two transformers'

        self.center_size = center_size
        self.num_img_token = num_img_token
        self.img_fcs = nn.ModuleList([nn.Linear(in_channels, self.embed_dims) for _ in range(self.num_transformer)])

    def extract_center_round_feat(self, x):
        pool_size = x.shape[-1]
        center_feat = x[..., (pool_size - self.center_size) // 2:(pool_size + self.center_size) // 2,
                      (pool_size - self.center_size) // 2:(pool_size + self.center_size) // 2]
        center_feat = torch.mean(center_feat, dim = [-2, -1])
        round_feat = (torch.sum(x, dim = [-2, -1]) - center_feat * self.center_size ** 2) / (
                pool_size ** 2 - self.center_size ** 2)

        return center_feat, round_feat

    def extract_img_token(self, x):
        img_token = x.view(x.shape[0], self.num_img_token, -1, *x.shape[2:])
        center_img_token, round_img_token = self.extract_center_round_feat(img_token)

        if self.num_transformer == 2:
            img_token = [center_img_token, round_img_token]
        elif self.num_transformer == 1:
            img_token = [torch.cat([center_img_token, round_img_token], dim = 1)]
        else:
            raise NotImplementedError

        return [self.img_fcs[i](token) for i, token in enumerate(img_token)]

    @staticmethod
    def extract_all_cls_tokens(tokens):
        return [torch.cat([t[:, 0] for t in token], dim = -1) for token in tokens]

    @staticmethod
    def extract_cls_token(token):
        return torch.cat([t[:, 0] for t in token], dim = -1)

    def token_forward(self, x, label = None):
        return self.fusion_transformer(self.fusion_transformer.embed_forward(self.extract_img_token(x)))

    def forward_train(self, img, gt_label, **kwargs):
        """Forward computation during training.

        Args:
            img (Tensor): of shape (N, C, H, W) encoding input images.
                Typically these should be mean centered and std scaled.
            gt_label (Tensor): It should be of shape (N, 1) encoding the
                ground-truth label of input images for single label task. It
                shoulf be of shape (N, C) encoding the ground-truth label
                of input images for multi-labels task.
        Returns:
            dict[str, Tensor]: a dictionary of loss components
        """
        if self.augments is not None:
            img, gt_label = self.augments(img, gt_label)

        x = self.extract_feat(img)
        if isinstance(x, tuple):
            x = x[-1]

        tokens = self.token_forward(x)
        cls_token = self.extract_cls_token(tokens[-1])

        return self.head.forward_train(cls_token, gt_label, **kwargs)

    def simple_test(self, img, img_metas = None, **kwargs):
        """Test without augmentation."""
        x = self.extract_feat(img)
        if isinstance(x, tuple):
            x = x[-1]
        tokens = self.token_forward(x)
        cls_token = self.extract_cls_token(tokens[-1])

        return self.head.simple_test(cls_token, **kwargs)
