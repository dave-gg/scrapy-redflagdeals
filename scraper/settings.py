# Scrapy settings for scrapeDeals project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scrapy-redflagdeals'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'
FEED_URI = 'deals.json'
FEED_FORMAT = 'json'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Google (+http://www.google.com)'
COOKIES_ENABLED = False
RETRY_ENABLED = False
DOWNLOAD_TIMEOUT = 15

LOG_ENABLED = False
