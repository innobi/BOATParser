import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(name='BOATParser',
      version='0.1.3',
      description='Business Objects Admin Tools Parser',
      long_description=README,
      author='Will Ayd',
      author_email='william.ayd@icloud.com',
      py_modules=['BOATParser'],
      install_requires=['pandas', 'lxml']
)
