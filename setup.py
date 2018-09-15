from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pybricks',
    version='0.0.1',
    url='https://github.com/emthomas/pybricks.git',
    author='Sebastien Thomas',
    author_email='titbabthomas@gmail.com',
    description='Python SDK for Databricks Rest API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], install_requires=['requests']
)
