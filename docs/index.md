# Project Template

This is a template for a python project with the following features:

- Pre-commit hooks for formatting, linting, style checking and commit messages checking. Check the `.pre-commit-config.yaml` file for all the hooks and their configurations.
- Unit tests with [pytest](https://docs.pytest.org/en/latest/) and coverage report with [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) support. We recommend you to add your tests under the `tests` folder for each module you write to make your code more robust.
- Auto-generated semantic version tags and the changelog file based on commit messages. This feature requires all the commit messages to follow the [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) style. Check the [version, tag and release document](get_started/contribution.md) on how to use this feature.
- Auto-build and release leveraging [hatch-vcs](https://github.com/ofek/hatch-vcs) to automatically generate semantic version tags and package versions. Remember to change the package name before you want to release it.
- Pre-written docs for installation and contribution, with [readthedocs](https://readthedocs.org/) support. Check the installation and contribution documents in the `docs/get_started` folder and the `.readthedocs.yaml` file for more details. We recommend you to write your own usage document under the `docs/usage` folder and also replace the `docs/index.md` file with your own readme document to introduce your project. Check the [document building section](get_started/usage.md) on how to leverage the readthedocs to build your documentation site.
- Github action support for all the above features including checking pre-commit hooks, unit tests and auto-releasing. Only the pre-commit hooks checker and unit tests are enabled by default, you can enable the auto-releasing github action by moving the `.github/examples/release.yml` to the `.github/workflows` folder.

Please read the [usage docs](get_started/usage.md) for more details on how to use this template project.

````{grid} 2
:gutter: 3

  ```{grid-item-card} Installation Guides

  Get started by installation.

  +++

    ```{button-ref} get_started/installation
    :expand:
    :color: secondary
    :click-parent:

    To the installation guides
    ```
  ```

  ```{grid-item-card} Usage Guides

  Details of the usages.

  +++

    ```{button-ref} get_started/usage
    :expand:
    :color: secondary
    :click-parent:

    To the Usage guides
    ```
  ```

  ```{grid-item-card} API Reference Guides

  References of the API.

  +++

    ```{button-ref} autoapi/project/index
    :expand:
    :color: secondary
    :click-parent:

    To the API Reference guides
    ```
  ```

  ```{grid-item-card} Contribution Guides

  Instruction to contribute to this project.

  +++

    ```{button-ref} get_started/contribution
    :expand:
    :color: secondary
    :click-parent:

    To the Contribution guides
    ```
  ```
````

```{toctree}
:hidden:
:caption: Get Started

get_started/installation
get_started/usage
get_started/contribution
get_started/changelog
```

```{toctree}
:hidden:
:caption: API References

autoapi/project/index
```
