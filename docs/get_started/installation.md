# Installation

## Prerequisites

We recommend you use `pixi` to install this project and all required packages with the specific version. If you don't have `pixi` installed, please install it first by referring to its official [docs](https://pixi.sh/latest/installation/). After that, you can use the rest of the document to install the project and all required packages.

However, if you don't want to use `pixi` and prefer to use `conda` and `pip`, you can also use them to install the project and all required packages. But you have to make sure the python version is compatible with the requirements of this project, which is specified in the `project.requires-python` field in the `pyproject.toml` file. Generally, we recommend you use the latest python version, if possible, for better performance.

In addition, this installation document is just for this project's users, instead of developers. If you want to develop based on this project or contribute to this project, please refer to the [development installation document](contribution.md#installation).

If you only want to use this project without developing or contributing to it, you can follow this document to install the project and all required packages.

### With `pixi`

If you have `pixi` installed, you can use the following command to install the project and all required packages.

```bash
pixi install -e base
```

After installation, you can use the following command to enter the project environment.

```bash
pixi shell -e base
```

### With `conda` and `pip`

If you don't want to use `pixi`, you can use `conda` and `pip` to install the project and all required packages by the following commands.

```bash
conda create -n <env_name> python=<python_version>
conda activate <env_name>
pip install -e .
```
