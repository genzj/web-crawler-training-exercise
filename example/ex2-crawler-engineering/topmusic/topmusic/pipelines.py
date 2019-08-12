# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem

sign_table = {
    u'白羊座': '火象',
    u'狮子座': '火象',
    u'射手座': '火象',
    u'水瓶座': '风象',
    u'双子座': '风象',
    u'天秤座': '风象',
    u'金牛座': '土象',
    u'处女座': '土象',
    u'摩羯座': '土象',
    u'巨蟹座': '水象',
    u'天蝎座': '水象',
    u'双鱼座': '水象',
}


class HoroscopeSignPipeline(object):
    def process_item(self, item, spider):
        if not item['horoscope']:
            raise DropItem('no horoscope')
        elif item['horoscope'] in sign_table:
            item['sign'] = sign_table[item['horoscope']]
        else:
            raise DropItem('invalid horoscope ' + item['horoscope'])
        return item
