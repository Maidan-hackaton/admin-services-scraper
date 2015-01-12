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
      list_urls = [
        "http://poslugy.gov.ua/AdminService/List?id=8903dcff-87ce-494f-8691-8fe2e940e1a0", # physichna
        "http://poslugy.gov.ua/AdminService/List?id=284411c3-1692-4ecb-9432-ac8aee0e86ed", # subject hospodaryuvannya
        "http://poslugy.gov.ua/AdminService/List?id=4ec58c04-9ca6-46c1-bc59-73d999c278c8" # juridychna
      ]
      for url in list_urls:
        yield self._build_request(url, self.parseList)
      item_urls = [
        "/AdminService/Details?id=ef00d7d3-48c4-40ed-85ee-c2bd0a151a8e",
        "/AdminService/Details?id=cd45bd02-e2d1-40e7-a492-b7b80a2b4e16"
      ]
      for url in item_urls:
        yield self._build_request("http://" + ServicesSpider.host + url, self.parseItem)

    def _build_request(self, url, parse):
        return Request(url=url, callback=parse)

    def parseList(self, response):
        #for item in [Service(name=e.extract().strip()) for e in response.css(".econtent::text")]:
        #  yield item
        for url in response.css(".ecell").xpath('@href').extract():
            yield self._build_request("http://poslugy.gov.ua" + url, self.parseItem)

    def parseItem(self, response):
        name = response.css(".tit div::text").extract()[0].strip()
        name = name.replace(u"\u00A0", ' ') # non-break space
        descriptions = response.css('.hsItemV')
        main_descriptions = descriptions[0].css('.lsti')
        recipients = map(lambda x: x.strip(), main_descriptions[1].css('ol li::text').extract())
        #main_descriptions[0].css()
        return Service(name=name, recipient=','.join(recipients))
