from get_index import BaiduIndex

if __name__ == "__main__":
    """
    可以传入很多关键词
    """
    # 查看城市和省份的对应代码
    # print(BaiduIndex.city_code)
    # print(BaiduIndex.province_code)

    # main
    keywords = ['爬虫', 'lol', '张艺兴', '人工智能', '华为', '武林外传']
    baidu_index = BaiduIndex(keywords, '2018-01-01', '2018-01-01')
    for index in baidu_index.get_index():
        print(index)