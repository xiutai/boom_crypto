import time
import requests
import re, threading
import redis

def write(data, file):
    with open(file, 'a+', encoding='utf-8') as f:
        f.writelines(data + '\n')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
proxies = {
    'http':'http://spjvwjqk0p:spjvwjqk0p@all.dc.smartproxy.com:10000',
    'https':'http://spjvwjqk0p:spjvwjqk0p@all.dc.smartproxy.com:10000'
}
def get_address(bnum):
    try:
        res = requests.get(
            'https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=1000&start=0&block=' + str(bnum), headers=headers, proxies=proxies)
        pattern = r'"(T[0-9A-Za-z]{33})"'
        addresses = re.findall(pattern, res.text)
        unique_addresses = list(set(addresses))
        return unique_addresses
    except Exception as e:
        write(f'id {bnum} 出现错误请及时检查问题!', 'err.txt')
        print(f'id {bnum} 出现错误请及时检查问题!', 'err.txt')
        return []

# 连接到Redis数据库
try:
    redis_conn = redis.StrictRedis(host='205.234.234.133', port=6379, decode_responses=True, password='boom_crypto')
except Exception as e:
    print('数据库连接失败，请检查!')
    exit()


# last_num = 0
# # 无限循环
# while True:
#     # 从Redis中获取最后记录的区块高度
#     last_recorded_block = redis_conn.get('last_recorded_block')
#     last_recorded_block = int(last_recorded_block) if last_recorded_block else 0
#     last_num = last_num if last_num else last_recorded_block
    
#     if last_num > last_recorded_block:
#         address = get_address(last_num)
#     else:
#         address = get_address(last_recorded_block)
    
#     for i in address:
#         # 使用Redis的集合数据结构来存储地址，确保地址唯一
#         redis_conn.sadd('addresses', i)
    
#     # 更新最后记录的区块高度
#     redis_conn.set('last_recorded_block', last_num)
    
#     print(f'当前正在同步第 {last_num} 个区块', address)
#     last_num += 1
#     # time.sleep(0.1)

num = int(redis_conn.get('block'))
count = redis_conn.scard('address')
print(f'当前已同步区块高度为: {num}, 已存储地址数量为: {count}')
# 多线程
def go():
    while True:
        global num
        s = num
        num+=1
        address = get_address(s)
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