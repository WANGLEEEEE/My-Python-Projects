import requests
import re
import json
import os
import time
def get_page(url):
    req = requests.get(url)
    if req.status_code == 200:
        req = req.text
        # html = req.encode(
        #     'ISO-8859-1').decode(
        #     requests.utils.get_encodings_from_content(req)[0])
        return req
    else:
        print('网页请求错误')

def parse_page(html):
    items = re.findall('"keys":(.*?),"data"',html,re.S)
    dic = json.loads(items[0])
    return dic

def CreateFile(title):
    isExists = os.path.exists(os.path.join("D:\LOL", title))
    if not isExists:
        print(u'建了一个名字叫做', title, u'的文件夹！')
        os.makedirs(os.path.join("D:\LOL", title))
        os.chdir(os.path.join("D:\LOL", title))  ##切换到目录
        return True
    else:
        print(u'名字叫做', title, u'的文件夹已经存在了！')
        return False

def save_pic(url,i):
    pic = requests.get(url).content
    with open(str(i+1) + '.jpg','ab') as file:
        file.write(pic)

if __name__ == '__main__':
    url = 'http://lol.qq.com/biz/hero/champion.js'
    html = get_page(url)
    datas = parse_page(html)


    for hero_id in datas.keys():
        CreateFile(hero_id)
        for i in range(20):
            if len(str(i)) == 1:
                pic_url = 'http://ossweb-img.qq.com/images/lol/web201310/skin/big' + str(hero_id) + '00' + str(i) + '.jpg'
            else:
                pic_url = 'http://ossweb-img.qq.com/images/lol/web201310/skin/big' + str(hero_id) + '0' + str(i) + '.jpg'

            save_pic(pic_url,i)
            time.sleep(1)





        #hero_url = 'http://lol.qq.com/biz/hero/' + str(hero_id) +'.js'

