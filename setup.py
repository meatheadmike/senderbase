from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='senderbase',
    version='0.1',
    description='A screen scraper for the senderbase.org website',
    long_description=long_description,
    url='https://github.com/meatheadmike/senderbase',
    author='Mike Skovgaard',
    author_email='mikesk@gmail.com',
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
    keywords='senderbase development email spam',
    packages=find_packages(exclude=['contrib', 'docs']),
    install_requires=['lxml','requests'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage','nose','unittest'],
    },
    py_modules=['senderbase'],
    test_suite="nose.collector"
)
