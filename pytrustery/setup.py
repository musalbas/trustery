from setuptools import setup

setup(
    name='trustery',
    version='0.1',
    packages=['trustery'],
    package_data={'trustery': ['trustery/trustery_abi.json']},
    install_requires=[
        'click',
        'jsonrpc-requests',
        'ethereum',
        'rlp',
        'configobj',
        'appdirs',
        'ethereum-rpc-client',
        'python-gnupg',
        'ipfs-api'
    ],
    entry_points='''
        [console_scripts]
        trustery=trustery.console:cli
    ''',
)
