from pymongo import MongoClient

COOKIES = 'BAIDUID=8759768F974CE3E6C2884260097331A4:FG=1; PSTM=1574683224; H_PS_PSSID=1445_21116_29567_29220; BIDUPSID=43233656E2011B10D268D7B02D7A956A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; PSINO=2; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1574939615; BDUSS=hWWDJ0Z01VOWZINGdPaWRkTUotYmR4WlRhcEhJNTVDQzA3SUpDNzBSWHRPQWRlRVFBQUFBJCQAAAAAAAAAAAEAAAA3VXuxu6rPxNPQxMzGpAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO2r313tq99daE; CHKFORREG=f47c79690c889b9fe3bb335ced026f76; bdindexid=j4g6p93elqe6o7phocmmfn53o2; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1574940479'

url_dic = {
    # 'day_all': 'https://www.bilibili.com/ranking/all/0/0/1',
    'day_origin': 'https://www.bilibili.com/ranking/origin/0/0/1',
    # 'day_cinema': 'https://www.bilibili.com/ranking/cinema/177/0/1',
    # 'day_rookie': 'https://www.bilibili.com/ranking/rookie/0/0/1',
}

user_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    # iPhone 6：
    "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",

]

video_detail_page_url = "https://www.bilibili.com/video/av"
video_data_page_url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid='
video_comment_url = "http://api.bilibili.com/x/reply?type=1&oid="
client = MongoClient("mongodb://localhost:27017")
video_rank = client["video"]['avnum_rank']
low_video_data_dbs = client["LowVideoData"]
high_video_data_dbs = client["HighVideoData"]

proxy = ["116.62.221.139:3128", "219.239.142.253:3128", "148.70.158.7:8080",
         "101.4.136.34:80", "116.62.240.1:3128", "119.41.236.180:8010", "116.62.234.0:3128", "116.62.189.215:3128"]

rank = {
    "动画一般": [78664865, 78661578, 78632284, 78614537, 78666019],
    "动画热门": [78204824, 78612134, 78607558, 78594045, 78600725],
    "音乐一般": [78639350, 78659447, 78667218, 78662794, 78662458],
    "音乐热门": [78535045, 78614476, 78581520, 78587059, 78613664],
    "舞蹈一般": [78665347, 78661315, 78666153, 78611358, 78666900],
    "舞蹈热门": [78591221, 78534287, 78615812, 78595171, 78584044],
    "游戏一般": [78666584, 78667233, 78666059, 78667408, 78666472],
    "游戏热门": [78589189, 78590596, 78613184, 78612469, 78616398],
    "科技一般": [78663513, 78552990, 78667931, 78660566, 78656740],
    "科技热门": [78605076, 78626170, 78625484, 78589763, 78458776],
    "数码一般": [78666337, 78665308, 78660804, 78660363, 78570608],
    "数码热门": [78501554, 78592020, 78578816, 78614161, 78627454],
    "生活一般": [78666243, 78669048, 78667266, 78669124, 78666226],
    "生活热门": [78613871, 78588498, 78351041, 78594403, 78608097],
    "鬼畜一般": [78656731, 78659334, 78659634, 78646086, 78636579],
    "鬼畜热门": [78583260, 78589061, 78594961, 78593563, 78584022],
    "娱乐一般": [78666050, 78668337, 78668014, 78666497, 78667982],
    "娱乐热门": [78593507, 78608417, 78582349, 78593748, 78584396],
    "全站日排行": [78530758, 78622872, 78595977, 78593791, 78553445]
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
}

video_type = [0, 1, 3, 4, 5, 11, 12, 13, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 36, 37, 39,
              41, 43, 46, 47, 50, 51, 53, 54, 56, 59, 60, 63, 65, 67, 71, 74, 75, 76, 77, 79, 80, 82, 83, 85, 86, 94,
              95, 96, 98, 114, 116, 118, 119, 120, 121, 122, 124, 125, 126, 127, 128, 129, 130, 131, 132, 134, 135, 136,
              137, 138, 139, 140, 141, 142, 143, 145, 146, 147]
