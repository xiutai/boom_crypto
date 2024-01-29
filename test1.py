import requests

proxies = {
    'http':'http://spjvwjqk0p:spjvwjqk0p@all.dc.smartproxy.com:10000',
    'https':'http://spjvwjqk0p:spjvwjqk0p@all.dc.smartproxy.com:10000'
}

res = requests.get('http://ipconfig.me',proxies=proxies)
print(res.text)