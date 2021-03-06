# -*- coding: utf-8 -*-

# Scrapy settings for dabi project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'me-gov-ua'

SPIDER_MODULES = ['me-gov-ua.spiders']
NEWSPIDER_MODULE = 'me-gov-ua.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'dabi (+http://www.yourdomain.com)'

HTTPCACHE_ENABLED = True
USER_AGENT = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS = 1
CONCURRENT_ITEMS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1

HTTPCACHE_IGNORE_HTTP_CODES = [403, 404, 500, 503]


ITEM_PIPELINES = {
    'me-gov-ua.pipelines.DuplicatesPipeline': 300,
}
