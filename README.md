# python-ethereum-block-validation-and-mining
Ethereum block mining and validation in Python implementation
This is a modification of the Py-EVM

Before running, please install>
pip3 install pyethash
Python3
and run the following commands> 
from web3 import IPCProvider, Web3
from web3.middleware import geth_poa_middleware
w3 = Web3(IPCProvider('/home/ubuntu/.ethereum/geth.ipc'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.clientVersion (to verify the connection and client version)
