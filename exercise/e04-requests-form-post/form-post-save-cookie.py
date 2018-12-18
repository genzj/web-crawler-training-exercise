# -*- encoding: utf-8 -*-

from __future__ import print_function
import requests
from bs4 import BeautifulSoup


def post_info(url, **kwargs):
    response = requests.post(url, kwargs)
    assert response.ok, 'status code %s - %s' % (response.status_code, response.reason)
    return BeautifulSoup(response.text, 'lxml').select_one('.flash').text.strip()

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

