from os import environ
from setuptools import setup

ci_environment = environ.get("CI", "false").lower() == "true"

local_scheme = "no-local-version" if ci_environment else "node-and-date"

setup(
    use_scm_version={
        "local_scheme": local_scheme,
    }
)