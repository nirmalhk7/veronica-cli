from setuptools import setup, find_packages
from veronica.cli import Veronica
import pickle
from pathlib import Path
from nltk.corpus import wordnet as wn

import warnings
warnings.filterwarnings("ignore")


def _post_install(setup):
    
    return setup


def _pre_install():

    return setup(
        name="veronica",
        version="0.2.9",
        description="",
        long_description=open('README.md').read(),
        long_description_content_type="text/markdown",
        author="Nirmal Khedkar",
        author_email="nirmalhk7@gmail.com",
        python_requires=">=3.6",
        license="MIT",
        packages=find_packages(),
        install_requires=[],
        entry_points={"console_scripts": [
            "veronica=veronica.cli:main", ], },
        include_package_data=True,
        package_data={'': ['data/*.veronica']}
    )


setup = _post_install(
    _pre_install()
)
