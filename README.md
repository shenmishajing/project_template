# Project Template

This template project is based on [pytorch lightning](https://pytorch-lightning.readthedocs.io/en/stable/) and [lightning-template](https://github.com/shenmishajing/lightning_template). Please read the docs of them before using this template.

## Installation

We recommend you use `conda` to install this project and all required packages with the specific version to recurrent our experiments and results of them. The following commands can be used to install this project and all required packages.

```bash
conda env create -f requirements/conda.yml -n <env_name>
conda activate <env_name>
pip install -e .
```

See [installation docs](docs/get_started/installation.md) for details.

## Usage

### Training

You can train the model with the following command.

```bash
CUDA_VISIBLE_DEVICES=<gpu_ids> cli fit --config-file configs/path/to/config.yaml
```
where the `configs/path/to/config.yaml` is the path to the config file you want to use.

### Evaluation

You can evaluate your model trained in the previous step on validation or test dataset with the following command.

```bash
CUDA_VISIBLE_DEVICES=<gpu_ids> cli {validate, test} --config-file configs/path/to/config.yaml --ckpt_path work_dirs/<run_name>/<run_id>/checkpoints/<ckpt_name>.ckpt
```
where the `{validate, test}` determines the dataset you want to evaluate, the `configs/path/to/config.yaml` is the path to the config file you want to use, and the `work_dirs/<run_name>/<run_id>/checkpoints/<ckpt_name>.ckpt` is the path to the checkpoint you want to evaluate.

### Prediction

You can predict the outcome of the clinical trials and plot the weights of the Sparse Mixture-of-Experts and Mixture-of-Experts modules with the following command.

```bash
CUDA_VISIBLE_DEVICES=<gpu_ids> cli predict --config-file configs/path/to/config.yaml --ckpt_path work_dirs/<run_name>/<run_id>/checkpoints/<ckpt_name>.ckpt
```

Similarly, the `configs/path/to/config.yaml` is the path to the config file you want to use, and the `work_dirs/<run_name>/<run_id>/checkpoints/<ckpt_name>.ckpt` is the path to the checkpoint you want to predict.

## Contribution

See [contribution docs](docs/get_started/contribution.md) for details.
