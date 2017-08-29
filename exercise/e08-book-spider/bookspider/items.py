# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader

import re

START_CLASS_NAMES = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
}

class BookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field(
        output_processor=TakeFirst(),
    )
    availability = scrapy.Field(
        output_processor=TakeFirst(),
        serializer=bool,
    )
    stock = scrapy.Field(
        output_processor=TakeFirst(),
        serializer=int,
    )
    star = scrapy.Field(
        serializer=int,
    )


def extract_price(value):
    m = re.search(r'([0-9.]+)', value)
    if not m or len(m.groups([])) < 1:
        return None
    return float(m.group(1))


def extract_star(value):
    cls = value.split()
    s = 0

    if 'star-rating' not in cls:
        return None

    for w in cls:
        score = START_CLASS_NAMES.get(w.lower(), 0)
        if s < score:
            s = score

    return s


class BookItemLoader(ItemLoader):
    default_item_class = BookItem
    default_input_processor = MapCompose(unicode, lambda x: x.strip())
    default_output_processor = TakeFirst()

    price_in = MapCompose(extract_price)

    availability_in = MapCompose(lambda value: 'in stock' in str(value).lower())

    star_in = MapCompose(extract_star)

