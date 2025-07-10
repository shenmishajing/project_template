# Usage

## Installation

Check the [Development Installation document](contribution.md#installation) for how to install the project and all required packages.

### Generate the conda.yml

This project leverages [pixi](https://pixi.sh/latest/installation) to manage the dependencies and environments, which provides a lock file to help users install your project and all required packages with the same version as you have. However, maybe someone prefer to use conda environment to install your project and all required packages. If you want to spread out your project with specific conda environment, you may need a `conda.yml` to help users to create the same environment as you have. You can use the following command to export your conda environment to the `conda.yml`.

````{note}
Make sure you are in the correct conda environment before you run the following command.

You can enter the correct conda environment now by:

  ```bash
  conda activate <env_name>
  ```
````

```bash
conda env export --no-builds | grep -v "prefix" > requirements/conda.yml
```

## Usage

### Pre-commit Hooks

Pre-commit hooks are used to automatically format, lint your commit and check your commit messages. You can refer to [Code Style and Git Hooks document](contribution.md#code-style-and-git-hooks) on how to use them. You can also add or remove the pre-commit hooks in the `.pre-commit-config.yaml` file, if you want.

### Unit tests

We leverage [pytest](https://docs.pytest.org/en/latest/) and [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) to run the unit tests and generate the coverage report. You can refer to [Unit tests document](contribution.md#unit-tests) on how to use them to run the unit tests and generate the coverage report. We recommend you to add unit tests under the `tests` folder for each module you write to make your code more robust.

If you want to run the unit tests and generate the coverage report for each commit automatically, you have to follow the following steps:

- [Optional if your repo is public] Setup up your project on [codecov](https://app.codecov.io/) and set up the `CODECOV_TOKEN` secret for your project. You can skip this step if your project is public since the upload action of [codecov](https://app.codecov.io/) supports tokenless upload for public repo now. But if your project is private, it's required to set up the `CODECOV_TOKEN` secret for your project.
- [Optional] Enable the multi-version unit tests job `unit-tests-python-version` by uncommenting it in the `.github/workflows/unit_tests.yml` file. You can also add more versions or remove them if you want.
- Add unit tests in the `tests` folder following the [pytest](https://docs.pytest.org/en/latest/) style. Commit your changes and push them to the remote repo.
- Enable flag analysis in the `Flags` setting of your project on [codecov](https://app.codecov.io/).
- Done. You can see the test results and coverage reports in the [codecov](https://app.codecov.io/) dashboard.

### Commit messages and release

We recommend you follow the [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) style for commit messages. You can refer to [Version, Tag and Release document](contribution.md#version-tag-and-release) on how to write the commit messages more easily and how to use them to generate the changelog and semantic version automatically.

If you want to publish your project as a python package and also generate github release automatically, you have to follow the following steps:

- Make up a new name for your project.
- Modify the `project.name` and `project.authors` in `pyproject.toml` and rename the `src/project` folder.
- Add any content you want in the `src` folder.
- Move the `.github/examples/release.yml` and `.github/examples/pre_release.yml` to the `.github/workflows` folder.
- Commit your changes following the [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) style.
- Bump version by [commitizen](https://github.com/commitizen-tools/commitizen) using the `cz bump` command. A changelog file will be generated in the `docs/get_started` folder automatically according to your commit messages.
- Add your project as a publisher on [PyPI](https://pypi.org/) and [TestPyPI](https://test.pypi.org/) respectively. You should set up the `release.yml` for [PyPI](https://pypi.org/) and the `pre_release.yml` for [TestPyPI](https://test.pypi.org/).
- Push your changes and tags to the remote repo.

### Documentation

If you want to build a documentation site for your project, you have to follow the following steps:

- Import your project from [readthedocs](https://readthedocs.org/).
- In `Admin > Automation Rules` of the Setting of your project, add a new rule to automatically activate the new version when a new tag is published. The `Match` of the rule should be `SemVer versions`. The `Version type` should be `tag` and the `Action` should be `Activate version`.
- Make a new name `<project_name>` for your project.
- Modify the `project.name` and `project.authors` in `pyproject.toml`.
- Modify the API document index path in `docs/index.md` from `autoapi/project/index` to `autoapi/<project_name>/index`.
- Rewrite an introduction in `README.md` and copy it to `docs/index.md` to replace the original introduction.
- [Optional] Write the Usage in `docs/get_started/usage.md`. Add more docs as you want to the `docs/` folder and update the `toctree` in `docs/index.md`.
- Commit the changes and push them to the remote repo.
- Done. You have successfully deployed the documentation of your project, and you can see a new version when you push a new tag to the remote repo.
