# -*- encoding: utf-8 -*-

import urllib, urllib2

from bs4 import BeautifulSoup


def post_info(url, **kwargs):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    form_data = urllib.urlencode(kwargs)
    req = urllib2.Request(
        url,
        data=form_data,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        }
    )
    response = opener.open(req)
    assert response.code / 100 == 2, 'status code %s - %s' % (response.code, response.msg)
    return BeautifulSoup(response.read(), 'lxml').select_one('.flash').text.strip()

if __name__ == '__main__':
    res = post_info(
        'http://the-internet.herokuapp.com/authenticate',
        username='tomsmith',
        password='SuperSecretPassword!'
    )
    print res

    res = post_info(
        'http://the-internet.herokuapp.com/authenticate',
        username='user',
        password='password'
    )
    print res

