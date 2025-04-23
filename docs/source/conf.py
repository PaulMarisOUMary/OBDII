# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from obdii import __version__ as obdii_version

from dataclasses import asdict
from pathlib import Path
from sphinxawesome_theme import ThemeOptions # type: ignore
from sphinxawesome_theme.postprocess import Icons # type: ignore
from sys import path

path.insert(0, str(Path('.')))

project = "py-obdii"
copyright = "2025-present, PaulMarisOUMary"
author = "PaulMarisOUMary"
release = '.'.join(obdii_version.split('.')[:3])

branch = "main" if any(tag in release for tag in ['a', 'b', "rc"]) else release

repo_url = "https://github.com/PaulMarisOUMary/OBDII"
pypi_url = "https://pypi.org/project/py-obdii"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
    "sphinx.ext.napoleon",
    # "sphinx.ext.coverage",
    # "sphinx.ext.graphviz",
    # "sphinx.ext.todo",
    "sphinx_design",
]

templates_path = ["_templates"]
exclude_patterns = [
    "build",
]

autodoc_member_order = "bysource"

napoleon_numpy_docstring = True
napoleon_google_docstring = False

pygments_style = "sphinx"
pygments_style_dark = "github-dark"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "serial": ("https://pyserial.readthedocs.io/en/latest/", None),
}

extlinks = {
    "issue": (repo_url + "/issues/%s", "Issue #"),
    "pr": (repo_url + "/pull/%s", "PR #"),
}

master_doc = "index"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinxawesome_theme"

theme_options = ThemeOptions(
    show_prev_next=True,
    show_scrolltop=True,
    awesome_external_links=True,
    main_nav_links = {
        "Home": "https://py-obdii.readthedocs.io/en/latest",
        "Emulator": "https://py-obdii.readthedocs.io/en/latest/emulator.html",
        "API": "https://py-obdii.readthedocs.io/en/latest/api.html",
    },
    extra_header_link_icons={
        "repository on GitHub": {
            "link": repo_url,
            "icon": (
                '<svg height="26px" style="margin-top:-2px;display:inline" '
                'viewBox="0 0 44 44" fill="currentColor" xmlns="http://www.w3.org/2000/svg">'
                '<path fill-rule="evenodd" clip-rule="evenodd" d="M22.477.927C10.485.927.76 10.65.76 22.647c0 9.596 6.223 17.736 14.853 20.608 1.087.2 1.483-.47 1.483-1.047 0-.516-.019-1.881-.03-3.693-6.04 1.312-7.315-2.912-7.315-2.912-.988-2.51-2.412-3.178-2.412-3.178-1.972-1.346.149-1.32.149-1.32 2.18.154 3.327 2.24 3.327 2.24 1.937 3.318 5.084 2.36 6.321 1.803.197-1.403.759-2.36 1.379-2.903-4.823-.548-9.894-2.412-9.894-10.734 0-2.37.847-4.31 2.236-5.828-.224-.55-.969-2.759.214-5.748 0 0 1.822-.584 5.972 2.226 1.732-.482 3.59-.722 5.437-.732 1.845.01 3.703.25 5.437.732 4.147-2.81 5.967-2.226 5.967-2.226 1.185 2.99.44 5.198.217 5.748 1.392 1.517 2.232 3.457 2.232 5.828 0 8.344-5.078 10.18-9.916 10.717.779.67 1.474 1.996 1.474 4.021 0 2.904-.027 5.247-.027 5.96 0 .58.392 1.256 1.493 1.044C37.981 40.375 44.2 32.24 44.2 22.647c0-11.996-9.726-21.72-21.722-21.72"/>'
                '</svg>'
            ),
        },
        "project on PyPI": {
            "link": pypi_url,
            "icon": (
                '<svg height="26px" style="margin-top:-2px;display:inline" '
                'viewBox="0 0 32 32" fill="currentColor" xmlns="http://www.w3.org/2000/svg">'
                '<path d="M31.896 18.104v5.219l-4.495 1.636-0.104 0.072 0.067 0.052 4.6-1.676 0.036-0.047v-5.329l-0.073-0.047zM31.495 7.489l-4.052 1.48v5.213l4.453-1.62v-5.219zM31.896 17.943v-5.219l-4.448 1.62v5.219zM27.292 19.615v-5.213l-4.396 1.599v5.219zM22.713 26.661v-5.213l-4.416 1.604v5.219zM22.896 21.412v5.156l4.416-1.609v-5.156l-4.416 1.604zM25.683 23.917c-0.489 0.181-0.88-0.1-0.88-0.615 0-0.521 0.391-1.089 0.88-1.267 0.489-0.176 0.885 0.104 0.885 0.62 0 0.521-0.396 1.089-0.885 1.261zM17.636 12.421l0.484-0.176-4.38-1.6-4.433 1.615 0.141 0.052 4.245 1.548zM27.344 14.219v-5.219l-4.448 1.62v5.219zM22.745 15.891v-5.219l-4.401 1.604v5.213zM18.193 12.328l-4.448 1.62v5.219l4.448-1.62zM9.208 17.552l4.432 1.615v-5.219l-4.432-1.609zM13.787 10.495l4.375 1.593v-5.156l-4.375-1.593zM27.344 3.62l-4.423 1.609v5.219l4.423-1.609zM22.599 5.203l-4.301-1.563-4.36 1.589 4.303 1.563zM20.484 6.14l-2.161 0.792v5.156l4.423-1.609v-5.156zM19.964 9.844c-0.491 0.183-0.881-0.099-0.881-0.615 0-0.521 0.391-1.089 0.881-1.265 0.489-0.177 0.885 0.099 0.885 0.62 0 0.52-0.396 1.083-0.885 1.26zM13.64 24.547v-5.219l-4.432-1.615v5.219zM18.24 22.912v-5.219l-4.495 1.635v5.219zM18.344 22.869l4.396-1.599v-5.219l-4.396 1.599zM18.24 28.292l-4.495 1.635v-5.219h-0.105v5.219l-4.432-1.615v-5.219l-0.068-0.072-0.036-0.084-4.448-1.615v-5.26l0.047 0.016 4.38 1.593 0.021-0.104-4.349-1.584 4.349-1.577v-0.147l-4.344-1.583 4.344-1.584v1.167l0.104-0.072v-3.161l4.344 1.577 0.079-0.077-4.183-1.527-0.141-0.047 4.324-1.573v-0.115l-4.491 1.636v0.025l-0.036 0.027v2.025l-4.516 1.647v0.025l-0.036 0.027v5.344l-4.521 1.64v0.027l-0.031 0.025v5.323l0.031 0.052 4.537 1.652 0.011-0.011 0.009 0.016 4.532 1.651 0.011-0.011 0.009 0.016 4.532 1.645 0.021-0.011 0.015 0.011 4.599-1.672 0.037-0.052zM4.656 12.749l4.344 1.579-4.344 1.584zM4.531 26.615l-4.427-1.609v-5.219l4.427 1.609zM4.552 21.292l-4.349-1.579 4.349-1.583v3.167zM9.083 28.265l-4.427-1.609v-5.219l4.427 1.615zM31.719 7.245l-4.276-1.557v3.115zM27.183 3.527l-4.319-1.573-4.359 1.583 4.328 1.579z"/>'
                '</svg>'
            ),
        },
    },
)

html_static_path = ["_static"]
html_css_files = ["custom.css"]

html_theme_options = asdict(theme_options)
html_permalinks_icon = Icons.permalinks_icon

html_title = "OBDII"
html_meta = {
    "description": "A modern, easy to use, Python ≥3.8 library for interacting with OBDII devices.",
    "keywords": "OBD2, ELM327, python, automotive, py-obdii",
    "author": "PaulMarisOUMary",
}


path.insert(0, str(Path("..", "..", "obdii")))
