from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

classifiers = [
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'License :: OSI Approved :: Apache Software License',
]

version = '0.1.1'

setup(name='clean-text',
      version=version,
      description='Clean Your Text to Create Normalized Text Representations',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Johannes Filter',
      author_email='hi@jfilter.de',
      url='https://github.com/jfilter/clean-text',
      license='MIT',
      install_requires=['ftfy'],
      extras_require={'gpl': ['unidecode']},
      include_package_data=True,
      classifiers=classifiers,
packages=find_packages())
