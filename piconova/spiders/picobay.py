#! /usr/bin/env python
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from picolib import PicoSpider


class PirateSpider(PicoSpider):
	name = "picobay"
	start_urls = ["http://thepiratebay.se/browse"]
	allowed_domains = ["thepiratebay.se"]

	tor_links = '/torrent/'
	deny_rules = ('/img*', '/%0Ahttp://*')

	xpath_dict = {
		'title'    : ('//*[@id="title"]'),
		'seeds'    : ('//*[@id="details"]/dl[1]/dd[7]/text()', 
			      '//*[@id="details"]/dl[2]/dd[3]/text()',
			      '//*[@id="details"]/dl[1]/dd[8]//text()'),
		'magnet'   : ('//*[@id="details"]/div[3]/a[1]/@href',
			      '//*[@id="details"]/div[4]/a/@href',
	                      '/html/body/div[3]/div[2]/div/div/div/div[2]/div[10]/a/@href'),
		'torrent'  : ('//*[@id="details"]/div[4]/a[2]/@href',
			      '//*[@id="details"]/div[3]/a[2]/@href'),
		'category' : ('//*[@id="details"]/dl[1]/dd[1]/a'),
		'leech'    : ('//*[@id="details"]/dl[1]/dd[9]/text()',
			      '//*[@id="details"]/dl[2]/dd[4]/text()'),
		'size'     : ('//*[@id="details"]/dl[1]/dd[3]/text()',),
		'added'    : ('//*[@id="details"]/dl[1]/dd[5]/text()',
			      '//*[@id="details"]/dl[2]/dd[1]/text()'),
		'uploader' : ('//*[@id="details"]/dl[1]/dd[6]/a/text()',
			      '//*[@id="details"]/dl[2]/dd[2]/a/text()')
	}		
					 															
	rules = (
        Rule(SgmlLinkExtractor(allow=('/torrent/',),), callback='parse_torrent', follow=True),
        Rule(SgmlLinkExtractor(allow=('/browse/*/*/7',),), callback='tpb_category_org', follow=True),
        Rule(SgmlLinkExtractor(allow=('/browse/',),), callback='parse_category', follow=True)
	)

    # make torrent page requests from subcategories
	def tpb_category_org(self, response):
		slx = SgmlLinkExtractor()
		sub_list = slx.extract_links(response)
		sub_req = get_reqs(sub_list)
		m = self.make_requests_for_url(sub_req)
		return m


spider = PirateSpider()

