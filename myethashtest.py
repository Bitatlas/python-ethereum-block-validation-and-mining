#!/usr/bin/python3

import rlp
from Crypto.Hash import keccak
from rlp.sedes import BigEndianInt, big_endian_int, Binary, binary
from rlp import encode
from eth_utils import to_bytes, to hex
from web3 import IPCProvider, Web3

_BYTES = 4                    # bytes in word 
DATASET_BYTES_INIT = 2**30        # bytes in dataset at genesis 
DATASET_BYTES_GROWTH = 2**23      # dataset growth per epoch 
CACHE_BYTES_INIT = 2**24          # bytes in cache at genesis 
CACHE_BYTES_GROWTH = 2**17        # cache growth per epoch 
CACHE_MULTIPLIER=1024             # Size of the DAG relative to the cache 
EPOCH_LENGTH = 30000              # blocks per epoch 
MIX_BYTES = 128                   # width of mix 
HASH_BYTES = 64                   # hash length in bytes 
DATASET_PARENTS = 256             # number of parents of each dataset element 
CACHE_ROUNDS = 3                  # number of rounds in cache production 
ACCESSES = 64                     # number of accesses in hashimoto loop

address = Binary.fixed_length(20, allow_empty=True)
hash32 = Binary.fixed_length(32)
uint256 = BigEndianInt(256)
trie_root = Binary.fixed_length(32, allow_empty=True)

class MiningBlockHeader(rlp.Serializable):
    fields = [
        ('parent_hash', hahs32),
        ('uncles_hash', hahs32),
        ('coinbase', address),
        ('state_root', trie_root),
        ('transaction_root', trie_root),
        ('bloom', uint256),
        ('difficulty', big_endian_int),
        ('block_number', big_endian_int),
        ('gas_limit', big_endian_int),
        ('gas_used', big_endian_int),
        ('timestamp', big_endian_int),
        ('extra_data', binary),
        #('mix_hash', binary), we have removed these 2 fields because we want a mining block header only
        #('nonce', Binary(8, allow_empty=True)
    ]

provider = Web3.IPCProvider('/home/ubuntu/.ethereum/geth.ipc')
w3 = Web3(provider)
assert w3.isConnected()

blockNumber = int(sys.argv[1], 10)

 myHeader = MiningBlockHeader(
     parent_hash = to_bytes(int(w3.eth.getBlock(blockNumber).parentHash.hex(), 16)),
     uncles_hash = to_bytes(int(w3.eth.getBlock(blockNumber).sha3Uncles.hex(), 16)),
     coinbase = to_bytes(int(w3.eth.getBlock(blockNumber).miner, 16)),
     state_root = to_bytes(int(w3.eth.getBlock(blockNumber).stateRoot.hex(), 16)),
     transaction_root = to_bytes(int(w3.eth.getBlock(blockNumber).transactionsRoot.hex(), 16)),
     receipt_root = to_bytes(int(w3.eth.getBlock(blockNumber).receiptsRoot.hex(), 16)),
     bloom = int(w3.eth.getBlock(blockNumber).logsBloom.hex(), 16),
     difficulty = w3.eth.getBlock(blockNumber).difficulty,
     block_number = w3.eth.getBlock(blockNumber).number,
     gas_limit = w3.eth.getBlock(blockNumber).gasLimit,
     gas_used = w3.eth.getBlock(blockNumber).gasUsed,
     timestamp = w3.eth.getBlock(blockNumber).timestamp,
     extra_data = to_bytes(int(w3.eth.getBlock(blockNumber).extraData.hex(), 16)),
     #mix_hash = to_bytes(int(w3.eth.getBlock(blockNumber).mixHash.hex(), 16)),
     #nonce = to_bytes(int(w3.eth.getBlock(blockNumber).nonce.hex(), 16)),
     
 )
