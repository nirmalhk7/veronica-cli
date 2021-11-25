from setuptools import setup, find_packages
from veronica.cli import Veronica
import pickle
from pathlib import Path
from nltk.corpus import wordnet as wn

import warnings
warnings.filterwarnings("ignore")


def _post_install(setup):
    method_names = [attr[3:] for attr in dir(Veronica) if attr[:3] == "do_"]
    print(method_names)
    synsets_all = {}

    for method in method_names:
        method_synsets = wn.synsets(method)
        for synset in method_synsets:
            synsets_all[(synset.name().split('.')[1],
                         synset.offset())] = method

    with open(Path.home()/".veronica.config", 'wb') as cn:
        pickle.dump(synsets_all, cn)

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
            "veronica_dev=veronica.cli:main", ], },
        include_package_data=True,
        package_data={'': ['data/*.veronica']}
    )


setup = _post_install(
    _pre_install()
)
