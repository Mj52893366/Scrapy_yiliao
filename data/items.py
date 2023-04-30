# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XywyDataItem(scrapy.Item):
    name = scrapy.Field()
    introduction = scrapy.Field()
    department = scrapy.Field()
    population = scrapy.Field()
    complication = scrapy.Field()
    symptom = scrapy.Field()
    inspect = scrapy.Field()
    medication = scrapy.Field()
    cause = scrapy.Field()
    pass

class HaoDaiFuItem(scrapy.Item):
    name = scrapy.Field()
    altname = scrapy.Field()
    department = scrapy.Field()
    introduction = scrapy.Field()
    cause = scrapy.Field()
    symptom = scrapy.Field()
    prevent = scrapy.Field()
    inspect = scrapy.Field()
    treatment = scrapy.Field()
    nutrition_and_diet = scrapy.Field()
    notice = scrapy.Field()
    prognosis = scrapy.Field()
    pass

class a39Item(scrapy.Item):
    name = scrapy.Field()
    introduction = scrapy.Field()
    altname = scrapy.Field()
    pathogenic_site = scrapy.Field()
    department = scrapy.Field()
    population = scrapy.Field()
    symptom = scrapy.Field()
    inspect = scrapy.Field()
    complication = scrapy.Field()
    treatment = scrapy.Field()
    pass

