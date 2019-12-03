# encoding:utf-8
import requests  # 导入requests模块用于访问测试自己的ip
from random import choice


proxy = ["116.62.221.139:3128", "82.137.244.151:8080", "219.239.142.253:3128", "148.70.158.7:8080", "124.156.108.71:82",
         "101.4.136.34:80", "116.62.240.1:3128", "119.41.236.180:8010", "116.62.234.0:3128", "116.62.189.215:3128"]

head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
     (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

url = 'http://www.bilibili.com/'
request = requests.get(url, proxies={'http': choice(pro)}, headers=head)
request.encoding = request.apparent_encoding
print(request.text)  # 输出返回的内容
