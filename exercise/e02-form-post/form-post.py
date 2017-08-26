# -*- encoding: utf-8 -*-

from __future__ import print_function
from __future__ import print_function
import urllib, urllib2


def post_info(url, **kwargs):
    opener = urllib2.OpenerDirector()
    opener.add_handler(urllib2.HTTPHandler())
    form_data = urllib.urlencode(kwargs)
    req = urllib2.Request(
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

