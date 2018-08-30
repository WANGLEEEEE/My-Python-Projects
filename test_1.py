import requests
from urllib.parse import urlencode
import os
from hashlib import md5
#请求网页
def get_page(offset):
    params = {
        'offset': offset,
        'format': 'json',
        'keyword':'街拍',
        'autoload':'true',
        'count':'20',
        'cur_tab':'1',
        'from':'seach_tab',
    }
    url = 'https://www.toutiao.com/search_content/?'+ urlencode(params)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            res = response.json()
            return res
    except requests.ConnectionError:
        print('请求超时')
        return None
#解析网页
def get_image(html):
    if html.get('data'):
        for item in html.get('data'):
            title = item.get('title')
            images = item.get('image_detail')
            for image in images:
                yield {
                    'image': image.get('url'),
                    'title': title
                }
#保存图片
def save_image(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(item.get('title'),
                                             md5(response.content).hexdigest(),
                                             'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')

def main():
    offset = 0
    html = get_page(offset)
    print(html)
main()
