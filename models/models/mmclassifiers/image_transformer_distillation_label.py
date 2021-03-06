# Copyright (c) OpenMMLab. All rights reserved.
import torch
from mmcls.models import build_loss
from torch import nn

from .image_transformer import ImageTransformerClassifier
from .image_transformer_with_label import ImageTransformerWithLabelClassifier


class ImageTransformerDistillationLabelTeacherClassifier(ImageTransformerWithLabelClassifier):
    def distillation_forward(self, img, label):
        x = self.extract_feat(img)
        if isinstance(x, tuple):
            x = x[-1]

        tokens = self.token_forward(x, label)
        return self.extract_all_cls_tokens(tokens)


class ImageTransformerDistillationLabelClassifier(ImageTransformerClassifier):
    def __init__(self,
                 teacher_classifier: nn.Module = None,
                 distillation_loss = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.teacher_classifier = teacher_classifier
        self.train_teacher = self.teacher_classifier.init_cfg is None
        if not self.train_teacher:
            for p in self.teacher_classifier.parameters():
                p.requires_grad = False

        if distillation_loss is not None:
            self.distillation_loss = build_loss(distillation_loss)

    def forward_train(self, img, label, gt_label, **kwargs):
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

        tokens = self.token_forward(x, label.to(x.dtype))
        cls_token = self.extract_all_cls_tokens(tokens)
        distillation_cls_token = self.teacher_classifier.distillation_forward(img, label.to(x.dtype))

        losses = dict()
        losses['loss_cls'] = self.head.forward_train(cls_token[-1], gt_label, **kwargs)['loss']
        losses['loss_distillation'] = torch.mean(
            torch.stack([self.distillation_loss(t, d) for t, d in zip(cls_token, distillation_cls_token)]))
        if self.train_teacher:
            losses['loss_teacher'] = self.teacher_classifier.forward_train(img, label, gt_label, **kwargs)['loss']
        return losses
