from scrapy.spiders import Spider
from scrapy.selector import Selector
from scraper.items import DealItem
from scrapy.http import Request

import yaml

config = yaml.safe_load(open("config.yml"))


class DealsSpider(Spider):
    # XPATH Constants
    DEAL_TOPIC_XPATH = '//h3[@class="topictitle"]'
    DEAL_TITLE_XPATH = './/a/text()'
    TOPIC_URL_XPATH = './/a/@href'

    POST_DATE_XPATH = '//span[@class="dateline_timestamp"]/text()'
    POST_DESCRIPTION_XPATH = '//div[@class="post_content"]/div[@class="content"]'
    POST_BY_XPATH = '//a[@class="postauthor"]/text()'
    POST_DEAL_URL_XPATH = '//dl[@class="post_offer_fields"]//a[@class="autolinker_link"]/@href'
    POST_PRICE_XPATH = '//div[@class="dealcontent"]/strong[text()="Price:"]/following-sibling::text()[1]'

    base_url = str(config['scrapy']['base_url'])

    name = 'deals'
    allowed_domains = [config['scrapy']['allowed_domains']]

    def __init__(self, forums, *args, **kwargs):
        super(DealsSpider, self).__init__(*args, **kwargs)
        for f in forums:
            self.start_urls.append(self.base_url + "/" + f + "/")

    def parse(self, response):
        sel = Selector(response)
        deals = sel.xpath(self.DEAL_TOPIC_XPATH)
        deal_items = []

        for deal in deals:
            deal_item = DealItem()
            try:
                deal_item['title'] = deal.xpath(self.DEAL_TITLE_XPATH).extract()[0]
                deal_item['title'] = deal_item['title'].replace('\n', '').strip()
            except IndexError:
                pass
            try:
                deal_item['url'] = deal.xpath(self.TOPIC_URL_XPATH).extract()[0]
            except:
                pass
            forum = response.request.url
            try:
                forum = forum[31:].strip('/')
            except IndexError:
                print("Could not find forum.")
            deal_item['forum'] = forum
            url = self.base_url + '/' + deal_item['url']
            yield Request(url=url, meta={'deal_item': deal_item}, callback=self.parse_item_page)

    def parse_item_page(self, response):
        sel = Selector(response)
        deal_item = response.meta['deal_item']
        try:
            deal_item['firstpostdate'] = sel.xpath(self.POST_DATE_XPATH).extract_first()
        except IndexError:
            print("Could not find firstpostdate")
        try:
            deal_item['description'] = sel.xpath(self.POST_DESCRIPTION_XPATH).extract_first()
            # Strip HTML tags from description
            deal_item['description'] = deal_item['description'].strip('<div class="content">').strip('</div>')
        except IndexError:
            pass
        try:
            deal_item['postedby'] = sel.xpath(self.POST_BY_XPATH).extract()[0]
        except IndexError:
            pass
        try:
            deal_item['deal_link'] = sel.xpath(self.POST_DEAL_URL_XPATH).extract()[0]
        except IndexError:
            pass
        try:
            deal_item['price_posted'] = sel.xpath(self.POST_PRICE_XPATH).extract()[0].strip()
        except IndexError:
            pass
        return deal_item
