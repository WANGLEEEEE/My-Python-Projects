import requests
import json
import os
import time


def get_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        req = response.text
        return req
    else:
        print('网页请求错误')
        return None

def CreateFile(title):
    isExists = os.path.exists(os.path.join("G:\王者荣耀", title))
    if not isExists:
        print(u'建了一个名字叫做', title, u'的文件夹！')
        os.makedirs(os.path.join("G:\王者荣耀", title))
        os.chdir(os.path.join("G:\王者荣耀", title))  ##切换到目录
        return True
    else:
        print(u'名字叫做', title, u'的文件夹已经存在了！')
        return False

def save_pic(title,pic):
    with open(str(title) + '.jpg','ab') as f:
        f.write(pic)

if __name__ == '__main__':
    url = 'http://pvp.qq.com/web201605/js/herolist.json'
    html = get_page(url)
    list = json.loads(html)
    number = len(list)
    for i in range(number):
        ename = list[i]['ename']
        cname = list[i]['cname']
        CreateFile(cname)
        skin_name = list[i]['skin_name'].split('|')
        skin_len = len(skin_name)
        for j in range(skin_len):
            print('正在爬取%s的第%s张皮肤' %(cname,j+1))
            title = skin_name[j]
            skin_url = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/'+str(ename)+'/' +str(ename) + '-'+ 'bigskin-' + str(j+1) + '.jpg'
            pic = requests.get(skin_url).content
            save_pic(title,pic)
            time.sleep(1)








