import os.path
from setuptools import setup, find_packages


def read(fname):
    '''Utility function to read the README file.'''
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='git-jira-worklog',
    version='0.1',
    packages=find_packages(),
    author='Andrzej Pragacz',
    author_email='apragacz@o2.pl',
    description=(
        'A tool for showing the work done based on the commits log'
    ),
    license='MIT',
    keywords='git jira worklog',
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'console_scripts': [
            'git-jira-worklog = jira_worklog.core:entry_point',
        ],
    },
)
