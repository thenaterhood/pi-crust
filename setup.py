#!/usr/bin/env python

from setuptools import setup
import sys
import os

install_requires = [
    'RPi.GPIO'
    ]

test_requires = [
    ]

data_files=[]


setup(name='pi-crust',
    version='0.2.0',
    description='Wrappers to make working with the Raspberry Pi GPIO interface more efficient',
    author='Nate Levesque',
    author_email='public@thenaterhood.com',
    url='https://github.com/thenaterhood/pi-crust/archive/master.zip',
    install_requires=install_requires,
    tests_require=test_requires,
    entry_points={
        'console_scripts': [
            'picrust-bus = pi_crust.__main__:do_bus',
            'picrust-parallel = pi_crust.__main__:do_parallel'
        ]
    },
    test_suite='nose.collector',
    package_dir={'':'src'},
    packages=[
        'pi_crust'
        ],
    data_files=data_files,
    package_data={
        }
    )
