# -*- coding: utf-8 -*-
import requests

if __name__ == '__main__':
    url = 'http://www.webtretho.com/forum/f90/13-dau-hieu-mang-thai-thuong-gap-nhat-1777446/'
    client = requests.Session()
    r = client.get(url)
    html = r.text
    print html.encode('utf-8')