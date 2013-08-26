from setuptools import setup
from setuptools import find_packages
import os

setup(
    name='django-factory-boy-command',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'factory-boy>=2.1.2',
        'Django>=1.4'
    ],
    author='Zenobius Jiricek',
    author_email='airtonix@gmail.com',
    description='Simple django management command for factory-boy',
    license='MIT',
    keywords='django, fixtures, mockups, factory-boy',
    url='https://github.com/airtonix/factory-boy-command',
    include_package_data=True,
)

