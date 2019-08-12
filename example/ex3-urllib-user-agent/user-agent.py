# -*- encoding: utf-8 -*-

from __future__ import print_function
from __future__ import print_function
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
from bs4 import BeautifulSoup


def read_user_agent(req=None):
    if req is None:
        req = Request('http://www.whatsmyua.info/')
    response = urlopen(req)
    assert response.code / 100 == 2, \
        'status code %s - %s' % (response.code, response.msg)
    bs = BeautifulSoup(response.read(), 'lxml')
    return (
        bs.select_one('#custom-ua-string').text,
        bs.select_one('#family').text
    )


if __name__ == '__main__':
    user_agent = read_user_agent()
    print('Original user-agent is:', user_agent)

    _req = Request(
        'http://www.whatsmyua.info/',
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3192.0 Safari/537.36'
        }
    )
    user_agent = read_user_agent(_req)
    print('Now user-agent is:', user_agent)
