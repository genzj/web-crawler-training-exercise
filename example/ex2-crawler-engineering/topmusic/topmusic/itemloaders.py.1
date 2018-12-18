from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose

from .items import SingerHoroscopeItem

class SingerHoroscopeItemLoader(ItemLoader):
    default_item_class = SingerHoroscopeItem

    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    rank_in = MapCompose(int)

    @staticmethod
    def parse_singer_page(response):
        loader = SingerHoroscopeItemLoader(response=response)
        loader.add_css('horoscope', 'span.birth', re=u'..座')
        loader.add_value('horoscope', '-')
        loader.add_css('singer', '.artist-name::text')
        loader.add_value('rank', response.meta['song']['rank'])
        loader.add_value('title', response.meta['song']['title'])
        return loader.load_item()

