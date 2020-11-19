from setuptools import setup, find_packages

setup(
    name="veronica",
    version='0.2.8',
    description="",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Nirmal Khedkar",
    author_email="nirmalhk7@gmail.com",
    python_requires=">=3.6",
    license="MIT",
    packages=find_packages(),
    entry_points={"console_scripts": ["veronica=veronica.cli:main",],},
    # packages=["veronica"]
)