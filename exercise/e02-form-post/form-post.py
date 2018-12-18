# -*- encoding: utf-8 -*-

from __future__ import print_function

try:
    from urllib.request import OpenerDirector, Request, HTTPHandler
except ImportError:
    from urllib2 import OpenerDirector, Request, HTTPHandler

try:
    from urllib.parse import urlencode as urlencode_
    urlencode = lambda data: urlencode_(data).encode('ascii')
except ImportError:
    from urllib import urlencode

def post_info(url, **kwargs):
    opener = OpenerDirector()
    opener.add_handler(HTTPHandler())
    form_data = urlencode(kwargs)
    req = Request(
        url,
        data=form_data,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        }
    )
    return opener.open(req)

if __name__ == '__main__':
    response = post_info(
        'http://the-internet.herokuapp.com/authenticate',
        username='tomsmith',
        password='SuperSecretPassword!'
    )
    print(response.code, response.headers.get('location'))

    response = post_info(
        'http://the-internet.herokuapp.com/authenticate',
        username='user',
        password='password'
    )
    print(response.code, response.headers.get('location'))

