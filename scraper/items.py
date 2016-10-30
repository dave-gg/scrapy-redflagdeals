# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class DealItem(Item):
    url = Field()
    forum = Field()
    title = Field()
    description = Field()
    firstpostdate = Field()
    postedby = Field()
    deal_link = Field()
    price_posted = Field()
