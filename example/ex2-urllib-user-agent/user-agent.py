# -*- encoding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup


def read_user_agent(req=None):
    if req is None:
        req = urllib2.Request('http://useragentstring.com/')
    response = urllib2.urlopen(req)
    assert response.code / 100 == 2, 'status code %s - %s' % (response.code, response.msg)
    bs = BeautifulSoup(response.read(), 'lxml')
    return bs.select_one('#uas_textfeld').text

if __name__ == '__main__':
    user_agent = read_user_agent()
    print 'Original user-agent is:', user_agent

    req = urllib2.Request(
        'http://useragentstring.com/',
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3192.0 Safari/537.36'
        }
    )
    user_agent = read_user_agent(req)
    print 'Now user-agent is:', user_agent
