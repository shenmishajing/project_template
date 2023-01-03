import os.path
import time
from types import MethodType
from typing import Any, Callable, Dict, Optional, Tuple, Type, Union

from pytorch_lightning.cli import (LightningArgumentParser, LightningCLI,
                                   SaveConfigCallback)

from utils.callbacks.save_and_log_config_callback import \
    SaveAndLogConfigCallback
from utils.optim import get_configure_optimizers_method

from .argument_parsers import ActionJsonFile
from .trainer import Trainer, _Trainer


class CLI(LightningCLI):
    def __init__(
        self,
        save_config_callback: Optional[
            Type[SaveConfigCallback]
        ] = SaveAndLogConfigCallback,
        trainer_class: Union[Type[_Trainer], Callable[..., _Trainer]] = Trainer,
        *args,
        **kwargs
    ) -> None:
        super().__init__(
            save_config_callback=save_config_callback,
            trainer_class=trainer_class,
            *args,
            **kwargs
        )

    def _setup_parser_kwargs(
        self, kwargs: Dict[str, Any], defaults: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        parser_kwargs = {"parser_mode": "mmengine_config"}
        main_kwargs, subparser_kwargs = super()._setup_parser_kwargs(kwargs, defaults)

        for k, v in parser_kwargs.items():
            main_kwargs.setdefault(k, v)
        for subcommand in self.subcommands():
            for k, v in parser_kwargs.items():
                if subcommand not in subparser_kwargs:
                    subparser_kwargs[subcommand] = {}
                subparser_kwargs[subcommand].setdefault(k, v)

        return main_kwargs, subparser_kwargs

    def add_default_arguments_to_parser(self, parser: LightningArgumentParser) -> None:
        super().add_default_arguments_to_parser(parser)
        parser.add_argument("--json", action=ActionJsonFile)
        parser.add_argument(
            "--optimizer_config",
            type=Optional[Dict],
            default=None,
            help="Configuration for the optimizers and lr schedulers.",
        )

    def before_instantiate_classes(self) -> None:
        """Implement to run some code before instantiating the classes."""
        super().before_instantiate_classes()
        config = (
            self.config["config"]
            if "subcommand" not in self.config
            else self.config[self.config["subcommand"]]
        )
        exp_name = os.path.splitext(os.path.split(config["config"][0].abs_path)[1])[0]
        exp_id = time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
        value_dict = {"name": exp_name, "version": exp_id}
        if (
            config.get("trainer") is not None
            and config["trainer"].get("logger") is not None
        ):
            if config["trainer"]["logger"].get("init_args") is None:
                config["trainer"]["logger"]["init_args"] = value_dict
            else:
                for k, v in value_dict.items():
                    if config["trainer"]["logger"]["init_args"].get(k) is None:
                        config["trainer"]["logger"]["init_args"][k] = v

    def _add_configure_optimizers_method_to_model(
        self, subcommand: Optional[str]
    ) -> None:
        super()._add_configure_optimizers_method_to_model(subcommand)
        optimizer_config = self._get(self.config_init, "optimizer_config")
        if optimizer_config:
            self.model.configure_optimizers = MethodType(
                get_configure_optimizers_method(optimizer_config), self.model
            )
