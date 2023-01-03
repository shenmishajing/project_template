from tkinter import N
from typing import Optional

from pytorch_lightning import Callback, LightningModule, Trainer
from pytorch_lightning.loggers.wandb import WandbLogger


class WandbLoggerLogAllCodeCallback(Callback):
    """Let wandb logger watch model when training starts."""

    def __init__(
        self,
        root: str = ".",
        name: str = None,
        include_exts: Optional[list] = None,
    ):
        self.root = root
        self.name = name

        if include_exts is None:
            include_exts = [".py", ".yaml", ".yml", ".sh", ".md"]
        self.include_exts = include_exts

    def setup(
        self, trainer: Trainer, pl_module: LightningModule, stage: Optional[str] = None
    ) -> None:
        if trainer.logger is not None and isinstance(trainer.logger, WandbLogger):
            if self.name is None:
                self.name = trainer.logger.experiment.project_name()
            trainer.logger.experiment.log_code(
                root=self.root,
                name=self.name,
                include_fn=lambda p: any(
                    [p.endswith(ext) for ext in self.include_exts]
                ),
            )
