# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '1.2.0'

setup(
    name='ple',
    version=version,
    description='App para la elaboracion de libros electronicos SUNAT PERU',
    author='seethersan',
    author_email='carlos_jcez@hotmail.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=("frappe","nubefact_integration"),
)
