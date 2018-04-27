from setuptools import setup

setup(name='oxt',
    version='0.1',
    description='A Python implementation of Searchable Encryption',
    url='https://github.com/Ning0Luo/OXT',
    author='Ning Luo',
    author_email='ning.luo@yale.edu',
    license='MIT',
    packages=['oxt'],
    install_requires=[
        'nltk',
        'crypto',
        'cryptography',
        'bitstring'
    ],
    zip_safe=False)