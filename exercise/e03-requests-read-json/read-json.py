# -*- encoding: utf-8 -*-

from __future__ import print_function
import requests


def read_json(url):
    response = requests.get(url)
    assert response.ok, \
        'status code %s - %s' % (
            response.status_code, response.reason
        )
    return response.json()


if __name__ == '__main__':
    photos = read_json(
        'http://www.nationalgeographic.com/photography/photo-of-the-day/_jcr_content/.gallery.json'
    )
    photo = photos['items'][0]
    print(
        photo['title'],
        photo['originalUrl']
    )
