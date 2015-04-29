from setuptools import setup, find_packages
from codecs import open
import os

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "version"), "r") as version_handle:
    version = version_handle.read().strip()

long_description = """
`Github <https://github.com/HurricaneLabs/opsgenie-python>`_
"""

setup(
	name = "opsgenie",
	version = version,
	description = "A Python client for the Opsgenie API",
    long_description = long_description,
	url = "https://github.com/HurricaneLabs/opsgenie-python",
	author = "Hurricane Labs",
	author_email = "colton@hurricanelabs.com",
	package_dir = {"":"src"},
	packages = find_packages("src"),
)

