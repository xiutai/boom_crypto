import os, sqlite3
from eth_keys import keys
from eth_keys.backends import NativeECCBackend
from tronpy.keys import PrivateKey

private_key = keys.PrivateKey(os.urandom(32), backend=NativeECCBackend)
def get_eth_address(priv_key):
    ethereum_address = priv_key.public_key.to_checksum_address()
    return ethereum_address

def get_tron_address(priv_key):
    priv_key = priv_key.to_hex()
    return PrivateKey(bytes.fromhex(priv_key[2:])).public_key.to_base58check_address()


private = private_key.to_hex()[2:]
eth_address= get_eth_address(private_key)
trx_address= get_tron_address(private_key)

# 连接到SQLite3数据库
def find_trx(address):
    conn = sqlite3.connect('tron_addresses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM addresses WHERE address=?", (address,))
    return cursor.fetchall()
print(f'当前生成的私钥: {private}')
print(f'当前生成的以太坊地址: {eth_address}')
print(f'当前生成的波场地址: {trx_address}')
# if find_trx(trx_address):
if find_trx('TJgmwx9TYaqujmdthJkjaLyWXrwTCmmTan'):
    print(f'私钥： {private}, 地址：{trx_address}, 撞库成功')
else:
    print(f'碰撞地址：{trx_address}, 不存在\n\n')