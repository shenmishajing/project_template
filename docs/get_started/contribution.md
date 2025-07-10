# Contribution

You are welcome to contribute to this project. We appreciate any contributions to this project.

Please follow the following steps to contribute to this project.
- Fork the repository.
- Clone the repository to your local machine.
- Create a new branch for your changes. Make sure you are in the correct branch before you make any changes.
- Install the project, all its required development dependencies and the pre-commit hooks following the [development installation document](#installation).
- Make your changes.
- Write the unit tests for all the changes you made.
- Run the unit tests and generate the coverage report to make sure your changes are correct.
- Write the documentation for all the changes you made.
- Build and preview the documentation to make sure it is correct.
- Commit your changes following the [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) style. The pre-commit hooks will be run automatically to check the code style and commit messages.
- Bump the version and generate the changelog automatically.
- Push your changes to the remote repository. The github action will be run automatically to check the unit tests and code style.
- Create a pull request to the main repository.
- Wait for the review and merge.
- Done. You have successfully contributed to this project.

We recommend you to write the unit tests and documentation for all the changes you made. This will help you to make sure your changes are correct and will help others to understand your changes.

In the following sections, we will introduce the details of key steps in the contribution process.

## Installation

First, you have to install the project, all its required development dependencies and the pre-commit hooks.

### Prerequisites

We recommend you use `pixi` to install this project and all required packages with the specific version. If you don't have `pixi` installed, please install it first by referring to its official [docs](https://pixi.sh/latest/installation/). After that, you can use the rest of the document to install the project and all required packages.

However, if you don't want to use `pixi` and prefer to use `conda` and `pip`, you can also use them to install the project and all required packages. But you have to make sure the python version is compatible with the requirements of this project, which is specified in the `project.requires-python` field in the `pyproject.toml` file. Generally, we recommend you use the latest python version, if possible, for better performance.

### With `pixi`

#### Install the project

If you have `pixi` installed, you can use the following command to install the project and all required packages.

```bash
pixi install -e all
```

#### Enter the project environment

After that, you can use the following command to enter the project environment and install the pre-commit hooks.

```bash
pixi shell -e all
```

Or if you are using `vscode` or other vscode forks, you can select the `'all': Pixi` interpreter in your python extension to enter the project environment automatically when you open a new terminal.

#### Install the pre-commit hooks

After entering the project environment, you can install the pre-commit hooks by the following command.

```bash
pre-commit install
```

#### Add more dependencies to the project environment

If you want to add more dependencies to the project environment, we recommend you to add them as pypi dependencies through `pixi` by the following command.

```bash
pixi add --pypi <package_name>
```

For conda dependencies, you can add them without the `--pypi` flag.

```bash
pixi add <package_name>
```

`pixi` will automatically add the dependencies and their versions to the `pyproject.toml` file and `pixi.lock` file. We recommend you to commit your `pixi.lock` file to the git repository to make sure the dependencies are installed consistently.

### With `conda` and `pip`

#### Install the project and pre-commit hooks

If you don't want to use `pixi`, you can use `conda` and `pip` to install the project and all pre-commit hooks by the following commands.

```bash
conda create -n <env_name> python=<python_version>
conda activate <env_name>
pip install -e . --group all
pre-commit install
```

#### Add more dependencies to the project environment

If you want to add development dependencies to the project environment, we recommend you to add them at the dependencies section of the `pyproject.toml` file first and then install them by the following command.

```bash
pip install -e . --group all
```

For conda dependencies, we recommend you first install all the conda dependencies before you install the project and all other pypi dependencies. If you want to add conda dependencies after you have installed pypi dependencies, we recommend you to remove the whole conda environment and create a new one.

## Unit Tests

We use [pytest](https://docs.pytest.org/en/latest/) and [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) to run the unit tests and generate the coverage report. We recommend you to add unit tests under the `tests` folder for each module you write. After that, you can use the following commands to run all your unit tests and generate the coverage report.

Run the unit tests by the following command.

```bash
pytest
```

Or run the unit tests with coverage.

```bash
pytest --cov=. --cov-branch
```

## Documents

We also recommend you to write documents under the `docs` folder for each module you write. After that, you can use the following command to build and preview your documents to make sure your documents are correct.

```bash
sphinx-autobuild docs docs/_build
```

## Code Style and Git Hooks

We leverage pre-commit hooks to make sure the code style and commit messages are consistent across all the contributors.

The code is formatted and linted by [ruff](https://github.com/astral-sh/ruff). The docstring is in [Google style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) and formatted by [docformatter](https://github.com/PyCQA/docformatter). The spelling is checked by [codespell](https://github.com/codespell-project/codespell). All commit messages should follow the [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) style to generate the changelog and semantic version automatically.

All the above requirements are checked by [pre-commit](https://pre-commit.com/) hooks automatically when you make a commit after you install the pre-commit hooks following the [installation section](installation.md). Make sure you have installed the pre-commit hooks before you make a commit.

If you run into any issues when you make a commit, it may be caused by you do not follow the code style or commit messages. You can run the pre-commit hooks manually by the following command to correct them.

```bash
pre-commit run --all-files
```

## Commit Messages, Version and Tags

We use [commitizen](https://github.com/commitizen-tools/commitizen) to bump the semantic version, create tags and generate the changelog automatically according to the commit messages. Then, [hatch-vcs](https://github.com/ofek/hatch-vcs) is used to generate the version number from the tags. Therefore, all commit messages should follow the [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) style to facilitate the version management tools.

Fortunately, the [commitizen](https://github.com/commitizen-tools/commitizen) and the [Commit Message Editor](https://marketplace.visualstudio.com/items?itemName=adam-bender.commit-message-editor) extension of [vscode](https://code.visualstudio.com/) can be used to generate the commit messages in the [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) style, which is helpful for writing the commit messages.

The whole process of a commit should be as follows:

- Install Commit Message Editor (Only the first time, optional). If you are using [vscode](https://code.visualstudio.com/) or other vscode forks, you can install the [Commit Message Editor](https://marketplace.visualstudio.com/items?itemName=adam-bender.commit-message-editor) extension to generate the commit message following the [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) style.
- Make changes. Do your changes and add the changes to the staging area.
- Commit changes. Then you can use `cz commit` to commit your changes. It will guide you to write the commit message in the [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) style. Or if you are using the [Commit Message Editor](https://marketplace.visualstudio.com/items?itemName=adam-bender.commit-message-editor) extension in vscode or other vscode forks, you can use it to generate the commit message and commit your changes.
- Bump version (Optional). If you have made some commits related to codes with `feat`, `fix`, `refactor`, `perf` or `BREAKING CHANGE` category, you should use `cz bump` to bump the version and generate the changelog automatically. Before you bump the version, stash all the changes to make sure your working directory is clean, since the bump process will commit all the changes in your working directory.
- Push changes. Then you can push your changes to the remote repo. If you have bumped the version, you should also push the tags to the remote repo by `git push --tags`. If you are using the [vscode](https://code.visualstudio.com/), you can set `git.followTagsWhenSync` to `true` to automatically push the tags when you sync your commits to the remote repo.
