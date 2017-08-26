# -*- encoding: utf-8 -*-

import urllib2
import json


def read_json(url):
    response = urllib2.urlopen(url)
    assert response.code / 100 == 2, 'status code %s - %s' % (response.code, response.msg)
    assert 'application/json' in response.headers.get('content-type').lower()
    return json.load(response)

if __name__ == '__main__':
    photos = read_json('http://www.nationalgeographic.com/photography/photo-of-the-day/_jcr_content/.gallery.json')
    photo = photos['items'][0]
    print(
        photo['title'],
        photo['url'] + photo['originalUrl']
    )