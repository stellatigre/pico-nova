#! /usr/bin/env python
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from items import Torrent

def make_requests_from_url(url):
    return Request(url, dont_filter=False, meta={'start_url': url})


def get_reqs(url_list):
    for next in url_list:
        return next.url

class PirateSpider(CrawlSpider):
    name = "picobay"
    start_urls = ["http://thepiratebay.se/browse"]
    allowed_domains = ["thepiratebay.se"]

	xpath_dict = {
		'title'    : ('//*[@id="title"]/text[]',),
		'seeds'    : ('//*[@id="details"]/dl[1]/dd[7]/text[]', 
				      '//*[@id="details"]/dl[2]/dd[3]/text[]',
				      '//*[@id="details"]/dl[1]/dd[8]//text[]'),
		'magnet'   : ('//*[@id="details"]/div[3]/a[1]/@href',
				      '//*[@id="details"]/div[4]/a/@href',
					  '/html/body/div[3]/div[2]/div/div/div/div[2]/div[10]/a/@href'),
		'torrent'  : ('//*[@id="details"]/div[4]/a[2]/@href',
					  '//*[@id="details"]/div[3]/a[2]/@href'),
		'category' : ('//*[@id="details"]/dl[1]/dd[1]/a/text()'),
		'leech'    : ('//*[@id="details"]/dl[1]/dd[9]/text()',
					  '//*[@id="details"]/dl[2]/dd[4]/text()'),
		'size'     : ('//*[@id="details"]/dl[1]/dd[3]/text()',),
		'added'    : ('//*[@id="details"]/dl[1]/dd[5]/text()',
					  '//*[@id="details"]/dl[2]/dd[1]/text()'),
		'uploader' : ('//*[@id="details"]/dl[1]/dd[6]/a/text()',
					  '//*[@id="details"]/dl[2]/dd[2]/a/text()')

	}		
					 															
    rules = (
        Rule(SgmlLinkExtractor(allow=('/torrent/',),), callback='parse_tpb_torrent', follow=True),
        Rule(SgmlLinkExtractor(allow=('/browse/*/*/7',),), callback='tpb_category_org', follow=True),
        Rule(SgmlLinkExtractor(allow=('/browse/',),), callback='parse_tpb_category', follow=True))

            # in this one, we're not making any requests, just links
    def parse_tpb_category(self, response):
        slx = SgmlLinkExtractor(allow='/torrent/', deny=('/img*', '/%0Ahttp://*'))
        sub_cats = slx.extract_links(response)
        for s in sub_cats:
            req = make_requests_from_url(s.url)
            return req

        # make torrent page requests from subcategories
    def tpb_category_org(self, response):
        slx = SgmlLinkExtractor()
        sub_list = slx.extract_links(response)
        sub_req = get_reqs(sub_list)
        m = make_requests_from_url(sub_req)
        return m

        # actual Pirate Bay torrent pages scraped here
    def parse_tpb_torrent(self, response):
        hxs = HtmlXPathSelector(response)
        page = Torrent()

		try_xpaths(page, self.xpath_dict, response)


spider = PirateSpider()

