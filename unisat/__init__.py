# Package information
__title__           = "unisat-connector-python"
__version__         = "0.0.42"
__description__     = "A lightweight library that works as a connector to UniSat API"
__url__             = "https://github.com/0X00db21/unisat-connector-python"
__author__          = "0xdb21"
__author_email__    = "contact@0xdb21.me"
__license__         = "BSD 3-Clause"
__keywords__        = "UniSat.io, API, Bitcoin, Ordinals, BRC20"
__platforms__       = "Windows, macOS, Linux"
__classifiers__     = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Topic :: Software Development :: Libraries :: Python Modules"
]

# Expose
from .client import Client
from .client import ClientError

# Constants
TESTNET = "https://open-api-testnet.unisat.io"
MAINNET = "https://open-api.unisat.io"
WHITELIST = "https://open-api-s1.unisat.io"
