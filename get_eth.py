import web3
import redis
import threading

# 连接到以太坊节点
w3 = web3.Web3(web3.HTTPProvider('https://eth.llamarpc.com'))

# 连接到Redis数据库
try:
    redis_conn = redis.StrictRedis(host='205.234.234.133', port=6379, decode_responses=True, password='boom_crypto', db=1)
except Exception as e:
    print('数据库连接失败，请检查!')
    exit()
num = int(redis_conn.get('block'))
count = redis_conn.scard('address')
print(f'当前已同步区块高度为: {num}, 已存储地址数量为: {count}')

def get_eth(num1):
    current_block = w3.eth.get_block(num1, True)
    addresses = []
    if current_block is not None:
        for tx in current_block.transactions:
            # 获取交易的发送者地址
            sender_address = tx['from']
            # 获取交易的接收者地址
            if 'to' in tx:
                receiver_address = tx['to']
            # 将地址添加到列表中，避免重复
            if sender_address not in addresses:
                addresses.append(sender_address)
            if receiver_address not in addresses:
                addresses.append(receiver_address)

    return list(addresses)

def go():
    while True:
        global num
        s = num
        num+=1
        address = get_eth(s)
        if address:
            try:
                redis_conn.sadd('address', *address)
                redis_conn.set('block',s)
            except Exception as e:
                print('写入redis服务器时报错  ',e)
        print(f'当前正在同步第 {s} 个区块', address)

threads = []
for x in range(5):  # 多线程开启
    t = threading.Thread(target=go)
    threads.append(t)
    t.start()
for t in threads:
    t.join()  # 等待所有线程执行完毕