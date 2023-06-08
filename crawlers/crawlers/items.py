# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ConjugationItem(scrapy.Item):
    infinitive = scrapy.Field()
    mood = scrapy.Field()
    tense = scrapy.Field()
    singular_first = scrapy.Field()
    singular_second = scrapy.Field()
    singular_third = scrapy.Field()
    plural_first = scrapy.Field()
    plural_second = scrapy.Field()
    plural_third = scrapy.Field()
