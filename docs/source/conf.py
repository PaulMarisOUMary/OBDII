# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from obdii import __version__ as obdii_version

from pathlib import Path
from sys import path


project = "py-obdii"
copyright = "2025-present, PaulMarisOUMary"
author = "PaulMarisOUMary"
release = '.'.join(obdii_version.split('.')[:3])

branch = "main" if any(tag in release for tag in ['a', 'b', "rc"]) else release

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
    "sphinx.ext.napoleon",
    # "sphinx.ext.coverage",
    # "sphinx.ext.graphviz",
    # "sphinx.ext.todo",
]

templates_path = ["_templates"]
exclude_patterns = [
    "build",
]


napoleon_numpy_docstring = True

pygments_style = "github-dark"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

extlinks = {
    "issue": ("https://github.com/PaulMarisOUMary/OBDII/issues/%s", "Issue #"),
    "pr": ("https://github.com/PaulMarisOUMary/OBDII/pull/%s", "PR #"),
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinxawesome_theme"
html_static_path = ["_static"]

html_title = "OBDII"


path.insert(0, str(Path("..", "..", "obdii")))