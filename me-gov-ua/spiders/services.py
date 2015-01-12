# -*- coding: utf-8 -*-
from scrapy import Spider, Item, Field, Selector, Request


class Service(Item):
  name = Field()
  recipient = Field()

class ServicesSpider(Spider):
    name = "services"
    host = "poslugy.gov.ua"
    allowed_domains = [host]

    def start_requests(self):
      initial_urls = [
        '/AdminService/List',
        '/AdminService/ListByType'
      ]
      for url in initial_urls:
        yield self._build_request(url, self.findUrls)

    def findUrls(self, response):
      for url in response.css(".ecell").xpath('@href').extract():
        if url.startswith('/AdminService/List'):
          yield self._build_request(url, self.findUrls)
        elif url.startswith('/AdminService/Details'):
          yield self._build_request(url, self.parseItem)

    def _build_request(self, url, parse):
        return Request(url='http://' + ServicesSpider.host + url, callback=parse)

    def parseItem(self, response):
        name = response.css(".tit div::text").extract()[0].strip()
        name = name.replace(u"\u00A0", ' ') # non-break space
        descriptions = response.css('.hsItemV')
        main_descriptions = descriptions[0].css('.lsti')
        recipients = map(lambda x: x.strip(), main_descriptions[1].css('ol li::text').extract())
        return Service(name=name, recipient=','.join(recipients))
