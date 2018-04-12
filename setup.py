import os

from setuptools import setup
from nifi_deploy import __version__


here = os.path.abspath(os.path.dirname(__file__))
readme = ''

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    readme = '\n' + f.read()

setup(
    name='nifi-deploy',
    version=__version__,
    description='Easy CLI tool for exporting and importing Nifi templates to and from XML files.',
    long_description=readme,
    url='https://pypi.org/project/nifi-deploy/',
    author='Mads H. Jakobsen',
    author_email='mads@hgaard.net',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: System :: Archiving :: Packaging',
        'Topic :: System :: Systems Administration',
    ],
    keywords='nifi deploy template nipyapi cli automation',
    packages=['nifi_deploy',],
    install_requires=[
        'nipyapi==0.8.0',
        'requests==2.18.4',
        'pyopenssl==17.5.0',
    ],
    entry_points={
        'console_scripts': [
            'nifi-deploy = nifi_deploy.nifi_deploy:cli',
        ]
    }
)
