import os
import eth_keys
from eth_keys import keys
from eth_keys.backends import NativeECCBackend
from tronapi import Tron

def generate_ethereum_and_tron_addresses():
    # 生成以太坊私钥
    private_key = os.urandom(32)
    eth_private_key = keys.PrivateKey(private_key, backend=NativeECCBackend)

    # 获取以太坊地址
    ethereum_address = eth_private_key.public_key.to_checksum_address()

    # 生成波场私钥
    tron = Tron()
    tron_private_key = tron.generate_address()
    tron_private_key_hex = tron_private_key.private_key

    # 获取波场地址
    tron_address = tron_private_key.address.base58

    return ethereum_address, tron_address, eth_private_key.to_hex(), tron_private_key_hex

ethereum_address, tron_address, eth_private_key, tron_private_key = generate_ethereum_and_tron_addresses()

print("以太坊地址:", ethereum_address)
print("波场地址:", tron_address)
print("以太坊私钥:", eth_private_key)
print("波场私钥:", tron_private_key)
