import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

setup(
    name='krock32',
    version='0.1.1',
    description='Base32 encoder/decoder using Crockford\'s alphabet',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/DrSLDR/krock32',
    author='Jonas A. Hultén',
    author_email='sldr@sldr.se',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8'
    ],
    packages=['krock32'],
    include_package_data=True
)
