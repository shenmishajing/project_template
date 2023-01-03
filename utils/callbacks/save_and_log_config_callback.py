import copy
from typing import Optional

from pytorch_lightning import LightningModule, Trainer
from pytorch_lightning.cli import SaveConfigCallback

from ..utils import get_log_dir


class SaveAndLogConfigCallback(SaveConfigCallback):
    """Saves and logs a LightningCLI config to the log_dir when training starts."""

    @staticmethod
    def process_config(config):
        # config = copy.deepcopy(config)
        # config["trainer"]["callbacks"] = [
        #     c.as_dict() for c in config["trainer"]["callbacks"]
        # ]
        return config

    def setup(
        self, trainer: Trainer, pl_module: LightningModule, stage: Optional[str] = None
    ) -> None:
        trainer.log_dir = get_log_dir(trainer)
        if trainer.logger is not None:
            trainer.logger.log_hyperparams(self.process_config(self.config))
        super().setup(trainer, pl_module, stage)
