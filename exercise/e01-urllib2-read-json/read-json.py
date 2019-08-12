# -*- encoding: utf-8 -*-

from __future__ import print_function
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import json


def read_json(url):
    response = urlopen(url)
    assert response.code / 100 == 2, \
        'status code %s - %s' % (response.code, response.msg)
    assert 'application/json' in response.headers.get('content-type').lower()
    return json.load(response)


if __name__ == '__main__':
    photos = read_json(
        'http://www.nationalgeographic.com/photography/photo-of-the-day/_jcr_content/.gallery.json'
    )
    photo = photos['items'][0]
    print(
        photo['title'],
        photo['originalUrl']
    )
