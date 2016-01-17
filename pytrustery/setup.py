from setuptools import setup

setup(
    name='trustery',
    version='0.1',
    packages=['trustery'],
    install_requires=[
        'click',
        'jsonrpc-requests',
    ],
    entry_points='''
        [console_scripts]
        trustery=trustery.console:cli
    ''',
)
