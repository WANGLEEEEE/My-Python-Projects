import requests
from requests.exceptions import RequestException
import re
import os
import time
#请求主网页
def get_page(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.text
        else:
            print('主网页请求错误')
            return None

    except RequestException:
        print('主网页请求是错误的')
        return None
#解析网页
def parse_page(html):
    items = re.findall('<li>.*?<span>.*?href="(.*?)".*?>(.*?)</a>.*?</li>',html,re.S)
    return items

#请求分页
def get_one_page(base_url):
    try:
        r = requests.get(base_url)
        if r.status_code == 200:
            return r.text
        else:
            print('分页请求错误')
            return None

    except RequestException:
        print('分页请求是错误的')
        return None

#解析分页
def parse_one_page(f_html):
    item = re.findall('<p>.*?src="(.*?)".*?</p>',f_html,re.S)
    return item

#保存图片
def save_image(j,title,img_url):
    name = title
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        'Referer': 'http://www.mzitu.com/',
    }
    img = requests.get(img_url,headers=headers)
    with open(str(j) +'.jpg','ab') as f:
         f.write(img.content)
#建立文件夹
def main(title):
    isExists = os.path.exists(os.path.join("D:\mzitu", title))
    if not isExists:
        print(u'建了一个名字叫做', title, u'的文件夹！')
        os.makedirs(os.path.join("D:\mzitu", title))
        os.chdir(os.path.join("D:\mzitu", title))  ##切换到目录
        return True
    else:
        print(u'名字叫做', title, u'的文件夹已经存在了！')
        return False

#主函数
if __name__ == '__main__':
    for i in range(1,25):
        url = 'http://www.mzitu.com/page/1'
        html = get_page(url)
        data = parse_page(html)
        title = data[i-1][1]
        main(title)
        for j in range(1,11):
            f_url = data[i-1][0] + '/' + str(j)
            f_html = get_one_page(f_url)
            img_url = parse_one_page(f_html)
            save_image(j,title, img_url[0])
            time.sleep(1)
            print('正在爬去第%s套图的第%s张~' %(i,j) )

        time.sleep(2)