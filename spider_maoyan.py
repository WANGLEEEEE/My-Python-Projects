import requests
import re
import json
import time
from requests.exceptions import RequestException
#请求网页
def get_one_page(url):

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        r = requests.get(url,headers = headers)
        if r.status_code == 200:
            return r.text
        else:
            print('请求错误')
            return None
    except RequestException:
        return None
#解析网页
def prase_one_page(html):
    items = re.findall('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
        + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
        + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',html,re.S)
    for item in items:
        yield {
            '排名': item[0],
            '图片': item[1],
            '片名': item[2],
            '主演': item[3].strip()[3:],
            '上映时间': item[4].strip()[5:],
            '评分': item[5] + item[6]
        }

#保存数据
def save_one_page(item):
    with open('猫眼电影排行榜.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')
#定义主函数
def main(offset):
    url = 'http://www.maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    data = prase_one_page(html)
    for item in data:
        save_one_page(item)

if __name__ == '__main__':
    for i in range(10):
        offset = i*10
        main(offset)
        print('正在爬取第%s页' %(i+1))
        time.sleep(1)
