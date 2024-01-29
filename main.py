import os
from eth_keys import keys
from eth_keys.backends import NativeECCBackend
from tronpy.keys import PrivateKey
import multiprocessing
import redis
import time

try:
    redis_conn_trx = redis.StrictRedis(host='localhost', port=6379, decode_responses=True, db=0)
except Exception as e:
    print('数据库连接失败，请检查!')
    exit()
try:
    redis_conn_eth = redis.StrictRedis(host='localhost', port=6379, decode_responses=True, db=1)
except Exception as e:
    print('数据库连接失败，请检查!')
    exit()

def find_trx(address):
    return redis_conn_trx.sismember('address', address)

def find_eth(address):
    return redis_conn_eth.sismember('address', address)

def write(data, file):
    with open(file, 'a+', encoding='utf-8') as f:
        f.writelines(data + '\n')

private_key = keys.PrivateKey(os.urandom(32), backend=NativeECCBackend)

def get_eth_address(priv_key):
    ethereum_address = priv_key.public_key.to_checksum_address()
    return ethereum_address

def get_tron_address(priv_key):
    priv_key = priv_key.to_hex()
    return PrivateKey(bytes.fromhex(priv_key[2:])).public_key.to_base58check_address()

def go(counter):
    while True:
        private = private_key.to_hex()[2:]
        eth_address = get_eth_address(private_key)
        trx_address = get_tron_address(private_key)
        
        if find_trx(trx_address):
            print(f'私钥： {private}, 地址：{trx_address}, 撞库成功')
            write(f'私钥： {private}, 地址：{trx_address}, 撞库成功', 'ok.txt')
        if find_eth(eth_address):
            print(f'私钥： {private}, 地址：{eth_address}, 撞库成功')
            write(f'私钥： {private}, 地址：{eth_address}, 撞库成功', 'ok.txt')
        
        counter.value += 1  # 更新共享的计数器值

if __name__ == "__main__":
    cpu_count = multiprocessing.cpu_count()
    counter = multiprocessing.Value('i', 0)  # 创建一个共享的整数计数器

    # 创建多个线程
    threads = []
    for i in range(cpu_count):
        thread = multiprocessing.Process(target=go, args=(counter,))
        threads.append(thread)

    # 启动所有线程
    for thread in threads:
        thread.start()

    while True:
        time.sleep(10)  # 每10秒钟打印一次统计信息
        print(f'每10秒钟运行 {counter.value} 次')  # 打印累计运行次数
        counter.value = 0