import torch
from lightning.pytorch import Callback


class SetFloat32MatmulPrecisionCallback(Callback):
    """
    Set float 32 matmul precision when training starts. For details, see
    https://pytorch.org/docs/stable/generated/torch.set_float32_matmul_precision.html
    """

    def __init__(
        self,
        percision: str = "highest",
    ):
        self.percision = percision

    def setup(self, *args, **kwargs) -> None:
        torch.set_float32_matmul_precision(self.percision)
