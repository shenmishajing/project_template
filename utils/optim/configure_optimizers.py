import copy
from typing import List, Sequence, Tuple, Union

from lightning.pytorch import LightningModule
from lightning.pytorch.cli import instantiate_class
from lightning.pytorch.utilities.types import LRSchedulerType
from torch.optim import Optimizer


def parser_optimizer_config(optimizer_config):
    optimizer_config = copy.deepcopy(optimizer_config)
    if not isinstance(optimizer_config, Sequence):
        optimizer_config = [optimizer_config]

    for i, optimizer_cfg in enumerate(optimizer_config):
        # parse the optimizer config
        if "optimizer" not in optimizer_cfg:
            optimizer_config[i] = {"optimizer": optimizer_cfg}
            optimizer_cfg = optimizer_config[i]

        if "lr_scheduler" in optimizer_cfg:
            if "scheduler" not in optimizer_cfg["lr_scheduler"]:
                optimizer_cfg["lr_scheduler"] = {
                    "scheduler": optimizer_cfg["lr_scheduler"]
                }
    return optimizer_config


def get_optimizer_parameters(model, num_optimizer):
    """
    Get all optimizer parameters.

    Args:
        model: a LightningModule.
        num_optimizer: number of optimizers.
    """
    optimizer_parameters = model.configure_optimizer_parameters()
    if optimizer_parameters is None:
        optimizer_parameters = [None] * num_optimizer
    assert isinstance(
        optimizer_parameters, list
    ), "optimizer_parameters should be None or list"
    if len(optimizer_parameters) < num_optimizer:
        optimizer_parameters += [None] * (num_optimizer - len(optimizer_parameters))

    return optimizer_parameters


def construct_optimizer(model, optimizer, params=None, set_lr=False):
    """
    Constructs the optimizer.

    Args:
        model: a LightningModule.
        params: a list of parameters to optimize, if None, all parameters of model will be optimized.
        optimizer: dictionary containing optimizer configuration.
        set_lr: whether to set the learning rate by the model.lr
    """
    if model.lr is not None and set_lr:
        if "init_args" not in optimizer:
            optimizer["init_args"] = {}
        optimizer["init_args"]["lr"] = model.lr
    optimizer = instantiate_class(
        model.parameters() if params is None else params, optimizer
    )
    if set_lr and model.lr is None:
        model.lr = optimizer.param_groups[0]["lr"]
    return optimizer


def construct_lr_scheduler(lr_scheduler, optimizer):
    """
    Constructs the lr_scheduler.

    Args:
        lr_scheduler: dictionary containing lr_scheduler configuration.
        optimizer: optimizer used to construct lr_scheduler.
    """

    # construct lr_scheduler
    lr_scheduler["scheduler"] = instantiate_class(optimizer, lr_scheduler["scheduler"])

    # construct warmup_lr_scheduler
    warmup_lr_scheduler = None
    if "warmup_config" in lr_scheduler:
        warmup_lr_scheduler = lr_scheduler.pop("warmup_config")
        if "scheduler" not in warmup_lr_scheduler:
            warmup_lr_scheduler = {
                "scheduler": {
                    "class_path": "utils.optim.WarmupScheduler",
                    "init_args": warmup_lr_scheduler,
                }
            }
        warmup_lr_scheduler.setdefault("frequency", 1)
        warmup_lr_scheduler["scheduler"] = instantiate_class(
            optimizer, warmup_lr_scheduler["scheduler"]
        )
    return lr_scheduler, warmup_lr_scheduler


def get_configure_optimizers_method(optimizer_config):
    def configure_optimizers(
        self: LightningModule,
    ) -> Union[Optimizer, Tuple[List[Optimizer], List[LRSchedulerType]]]:
        optimizer_cfg = parser_optimizer_config(optimizer_config)
        optimizer_parameters = get_optimizer_parameters(self, len(optimizer_cfg))
        manual_step_scedulers = []

        for i, cfg in enumerate(optimizer_cfg):
            # construct optimizer
            cfg["optimizer"] = construct_optimizer(
                self, cfg["optimizer"], optimizer_parameters[i], set_lr=i == 0
            )
            # construct lr_scheduler
            if "lr_scheduler" in cfg:
                cfg["lr_scheduler"], manual_lr_scheduler = construct_lr_scheduler(
                    cfg["lr_scheduler"], cfg["optimizer"]
                )

                if manual_lr_scheduler is not None:
                    manual_step_scedulers.append(manual_lr_scheduler)
        self.manual_step_scedulers = manual_step_scedulers
        return optimizer_cfg

    return configure_optimizers
