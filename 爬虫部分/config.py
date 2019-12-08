from pymongo import MongoClient

COOKIES = 'BIDUPSID=3D9FA239E62EAD6D69F71B04F456772F; PSTM=1571919122; BAIDUID=3D9FA239E62EAD6D5638B311B815367E:FG=1; BD_UPN=12314753; H_PS_PSSID=1424_21088_29567_29699_29220_26350; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDUSS=ttTkVQT1JyakZUVUFFTFB5dk4xOENWQ2NPWUdMUTB5SUd2VVctZXJoYTZoUGhkRVFBQUFBJCQAAAAAAAAAAAEAAABTIPQnNTI1M8ez0vcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALr30F2699BdcG; bdindexid=7gm3j2p7f3tmrvdhpd1d9lcqf7; BD_HOME=1; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; BD_CK_SAM=1; PSINO=1; H_PS_645EC=e6fbgyaAv7Ux5nX1nZa%2BYElECn8wZkOG7LHB10yUlcRz1swEjDIapo5dd53HhncvR6E3'

url_dic = {
    # 'day_all': 'https://www.bilibili.com/ranking/all/0/0/1',
    'day_origin': 'https://www.bilibili.com/ranking/origin/0/0/1',
    # 'day_cinema': 'https://www.bilibili.com/ranking/cinema/177/0/1',
    # 'day_rookie': 'https://www.bilibili.com/ranking/rookie/0/0/1',
}

head = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Cookie': COOKIES,
    'Pragma': 'no-cache',
    'Proxy-Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
             (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
}

video_detail_page_url = "https://www.bilibili.com/video/av"
video_data_page_url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid='
video_comment_url = "http://api.bilibili.com/x/reply?type=1&oid="
client = MongoClient("mongodb://localhost:27017")
video_rank = client["video"]['avnum_rank']
video_data_dbs = client["newVideoData"]

proxy = ["116.62.221.139:3128", "219.239.142.253:3128", "148.70.158.7:8080",
         "101.4.136.34:80", "116.62.240.1:3128", "119.41.236.180:8010", "116.62.234.0:3128", "116.62.189.215:3128"]
