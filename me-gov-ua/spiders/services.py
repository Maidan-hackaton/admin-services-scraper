# -*- coding: utf-8 -*-
from scrapy import Spider, Item, Field, Selector, Request


class Service(Item):
  name = Field()
  recipient = Field()


class ServicesSpider(Spider):
    name = "services"
    allowed_domains = ["poslugy.gov.ua"]

    def start_requests(self):
      url="http://poslugy.gov.ua/AdminService/List?id=8903dcff-87ce-494f-8691-8fe2e940e1a0"
      yield self._build_request(url, self.parseList)

    def _build_request(self, url, parse):
        return Request(url=url, callback=parse)

    def parseList(self, response):
        #for item in [Service(name=e.extract().strip()) for e in response.css(".econtent::text")]:
        #  yield item
        for url in response.css(".ecell").xpath('@href').extract():
            yield self._build_request("http://poslugy.gov.ua" + url, self.parseItem)

    def parseItem(self, response):
        name = response.css(".tit div::text").extract()[0].strip()
        descriptions = response.css('.hsItemV')
        main_descriptions = descriptions[0].css('.lsti')
        recipients = map(lambda x: x.strip(), main_descriptions[1].css('ol li::text').extract())
        return Service(name=name, recipient=','.join(recipients))
