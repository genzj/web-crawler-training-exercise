# -*- encoding: utf-8 -*-
from __future__ import print_function
from __future__ import generators
import requests
from bs4 import BeautifulSoup


def crawl_baidu_music():
    response = requests.get('http://music.baidu.com/top/dayhot')
    assert response.ok, \
        'status code %s - %s' % (response.status_code, response.reason)

    response.encoding = 'utf-8'
    page = BeautifulSoup(response.text, 'lxml')

    def extract_by_css(selector):
        return map(lambda i: i.text.strip(), page.select(selector))

    for rank, title, singer in zip(
        extract_by_css('.index-num.index-hook'),
        extract_by_css('.song-title > a:nth-of-type(1)'),
        extract_by_css('.author_list'),
    ):
        print('rank:', rank, 'title:', title, 'singer:', singer)
        yield rank, title, singer


if __name__ == '__main__':
    with open('output.txt', 'wb') as of:
        for rank, title, singer in crawl_baidu_music():
            of.write(u'|'.join([rank, title, singer]).encode('utf-8') + b'\n')
