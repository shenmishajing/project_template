import copy
import string
from abc import ABC
from collections.abc import Mapping, Sequence

from lightning.pytorch.core.datamodule import (
    LightningDataModule as _LightningDataModule,
)
from mmengine.dataset import COLLATE_FUNCTIONS
from mmengine.registry import DATASETS
from sklearn.model_selection import KFold
from torch.utils.data.dataloader import DataLoader
from torch.utils.data.dataset import Subset


class LightningDataModule(_LightningDataModule):
    SPLIT_NAMES = ["train", "val", "test", "predict"]

    def __init__(
        self,
        dataset_cfg,
        dataloader_cfg=None,
        split_format_to="ann_file",
        split_name_map=None,
    ):
        super().__init__()

        self.dataset_cfg = dataset_cfg
        self.split_format_to = (
            split_format_to
            if split_format_to is None or isinstance(split_format_to, list)
            else [split_format_to]
        )
        if split_name_map is None:
            self.split_name_map = {}
        else:
            self.split_name_map = split_name_map
        for name in self.SPLIT_NAMES:
            self.split_name_map.setdefault(name, name if name != "predict" else "test")

        self.dataloader_cfg = {} if dataloader_cfg is None else dataloader_cfg

        if all([self.dataloader_cfg.get(name) is None for name in self.SPLIT_NAMES]):
            self.dataloader_cfg = {
                name: self.dataloader_cfg for name in self.SPLIT_NAMES
            }

        self.datasets = {}
        self.dataset = None

    def _get_split_names(self, stage=None):
        if self.trainer.overfit_batches > 0:
            split_names = ["train"]
        elif stage is None:
            split_names = ["train", "val", "test", "predict"]
        elif stage == "fit":
            split_names = ["train", "val"]
        else:
            split_names = [stage.lower()]
        return split_names

    def _setup_dataset(self, split_name):
        self.datasets[split_name] = self._build_data_set(
            self.split_name_map[split_name]
        )

    def setup(self, stage=None):
        split_names = self._get_split_names(stage)

        for name in split_names:
            self._setup_dataset(name)
        self.dataset = self.datasets[split_names[0]]

    def _dataloader(self, split_name, **kwargs):
        return self._build_data_loader(
            self.datasets[split_name], split=split_name, **kwargs
        )

    def train_dataloader(self):
        return self._dataloader("train")

    def val_dataloader(self):
        return self._dataloader("val")

    def test_dataloader(self):
        return self._dataloader("test")

    def predict_dataloader(self):
        return self._dataloader("predict")

    def _build_data_set(self, split):
        cfg = copy.deepcopy(self.dataset_cfg)
        if self.split_format_to is None:
            cfg["split"] = split
        else:
            for s in self.split_format_to:
                cfg[s] = string.Template(cfg[s]).safe_substitute(split=split)

        # build dataset
        dataset = DATASETS.build(cfg)
        if hasattr(dataset, "full_init"):
            dataset.full_init()

        return dataset

    def _build_data_loader(self, dataset, split="train"):
        if isinstance(dataset, Mapping):
            return {
                key: self._build_data_loader(
                    ds,
                    split=split,
                )
                for key, ds in dataset.items()
            }
        elif isinstance(dataset, Sequence):
            return [
                self._build_data_loader(
                    dataset[i],
                    split=split,
                )
                for i in range(len(dataset))
            ]
        else:
            dataloader_cfg = copy.deepcopy(self.dataloader_cfg[split])
            collate_fn_cfg = dataloader_cfg.pop(
                "collate_fn", dict(type="default_collate")
            )
            collate_fn_type = collate_fn_cfg.pop("type")
            collate_fn = COLLATE_FUNCTIONS.get(collate_fn_type)
            collate_fn = partial(collate_fn, **collate_fn_cfg)  # type: ignore
            return DataLoader(dataset=dataset, collate_fn=collate_fn, **dataloader_cfg)


class KFoldLightningDataModule(LightningDataModule, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_folds = None
        self.folds = {}
        self.splits = []

    def _get_split_names(self, stage=None):
        if self.trainer.overfit_batches > 0:
            split_names = ["train"]
        elif stage is None:
            split_names = ["train", "val", "test", "predict"]
        elif stage == "fit":
            split_names = ["train"]
        else:
            split_names = [stage.lower()]
        return split_names

    def setup(self, stage=None):
        super().setup(stage)
        split_names = self._get_split_names(stage)
        if "train" in split_names or "val" in split_names:
            self.setup_folds(2)
            self.setup_fold_index(0)

    def setup_folds(self, num_folds: int) -> None:
        self.num_folds = num_folds
        self.splits = [
            split for split in KFold(num_folds).split(range(len(self.dataset)))
        ]

    def setup_fold_index(self, fold_index: int) -> None:
        for indices, fold_name in zip(self.splits[fold_index], ["train", "val"]):
            self.folds[fold_name] = Subset(self.dataset, indices)

    def _fold_dataloader(self, split_name, **kwargs):
        return self._build_data_loader(
            self.folds[split_name], split=split_name, **kwargs
        )

    def train_dataloader(self):
        return self._fold_dataloader("train")

    def val_dataloader(self):
        return self._fold_dataloader("val")
