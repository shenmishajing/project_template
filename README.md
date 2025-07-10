# Project Template

This is a template for a python project with the following features:

- Pre-commit hooks for formatting, linting, style checking and commit messages checking. Check the `.pre-commit-config.yaml` file for all the hooks and their configurations.
- Unit tests with [pytest](https://docs.pytest.org/en/latest/) and coverage report with [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) support. We recommend you to add your tests under the `tests` folder for each module you write to make your code more robust.
- Auto-generated semantic version tags and the changelog file based on commit messages. This feature requires all the commit messages to follow the [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) style. Check the [version, tag and release document](docs/get_started/contribution.md#version-tag-and-release) on how to use this feature.
- Auto-build and release leveraging [hatch-vcs](https://github.com/ofek/hatch-vcs) to automatically generate semantic version tags and package versions. Remember to change the package name before you want to release it.
- Pre-written docs for installation and contribution, with [readthedocs](https://readthedocs.org/) support. Check the installation and contribution documents in the `docs/get_started` folder and the `.readthedocs.yaml` file for more details. We recommend you to write your own usage document under the `docs/usage` folder and also replace the `docs/index.md` file with your own readme document to introduce your project. Check the [document building section](docs/get_started/usage.md#documentation) on how to leverage the readthedocs to build your documentation site.
- Github action support for all the above features including checking pre-commit hooks, unit tests and auto-releasing. Only the pre-commit hooks checker and unit tests are enabled by default, you can enable the auto-releasing github action by moving the `.github/examples/release.yml` to the `.github/workflows` folder.

## Installation

Check the [User installation document](docs/get_started/installation.md) for how to install the project and all required packages, if you only want to use this project without developing or contributing to it.

Check the [Development Installation document](docs/get_started/contribution.md#installation) for how to install the project and all required packages, if you want to develop based on this project or contribute to it.

## Usage

Check the [Usage document](docs/get_started/usage.md) for how to use the project template.

## Contribution

See [contribution docs](docs/get_started/contribution.md) for details.
