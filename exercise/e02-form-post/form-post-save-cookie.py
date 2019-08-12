# -*- encoding: utf-8 -*-

from __future__ import print_function
try:
    from urllib.request import build_opener, Request, HTTPCookieProcessor
except ImportError:
    from urllib2 import build_opener, Request, HTTPCookieProcessor

try:
    from urllib.parse import urlencode as urlencode_

    def urlencode(data):
        return urlencode_(data).encode('ascii')
except ImportError:
    from urllib import urlencode

from bs4 import BeautifulSoup


def post_info(url, **kwargs):
    opener = build_opener(HTTPCookieProcessor())
    form_data = urlencode(kwargs)
    req = Request(
        url,
        data=form_data,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        }
    )
    response = opener.open(req)
    assert response.code / 100 == 2, \
        'status code %s - %s' % (response.code, response.msg)
    return BeautifulSoup(
        response.read(), 'lxml'
    ).select_one(
        '.flash'
    ).text.strip()


if __name__ == '__main__':
    res = post_info(
        'http://the-internet.herokuapp.com/authenticate',
        username='tomsmith',
        password='SuperSecretPassword!'
    )
    print(res)

    res = post_info(
        'http://the-internet.herokuapp.com/authenticate',
        username='user',
        password='password'
    )
    print(res)
