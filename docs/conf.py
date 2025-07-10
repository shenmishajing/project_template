# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import tomllib
from datetime import datetime
from importlib.metadata import version as get_version

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------


def get_project_info_from_toml(file_path):
    """Get the project name and author from the pyproject.toml file.

    Args:
        file_path: The path to the pyproject.toml file.

    Returns:
        A dict of the project name and author.
    """
    try:
        with open(file_path, "rb") as f:
            data = tomllib.load(f)
        return {
            "name": data.get("project", {}).get("name"),
            "author": data.get("project", {}).get("authors", [{}])[0].get("name"),
        }
    except FileNotFoundError:
        print(f"Error: file '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error: failed to parse the toml file: {e}")
        return None


project_info = get_project_info_from_toml("../pyproject.toml")
project = project_info.get("name")
author = project_info.get("author")
year = datetime.now().year
copyright = f"{year}, {author}"

# The full version, including alpha/beta/rc tags
release: str = get_version(project)
# for example take major/minor
version: str = ".".join(release.split(".")[:2])


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "autoapi.extension",
    "myst_parser",
    "sphinx_design",
]

autoapi_dirs = [f"../src/{project}/"]
autoapi_add_toctree_entry = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
