#! /usr/bin/env python
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field
from scrapy.http import Request
from items import Torrent
from multiprocessing import Process
import celery


def make_requests_from_url(url):
    return Request(url, dont_filter=False, meta={'start_url': url})


def get_reqs(url_list):
    for next in url_list:
        return next.url


class PirateSpider(CrawlSpider):
    name = "picobay"
    start_urls = ["http://thepiratebay.se/browse"]
    allowed_domains = ["thepiratebay.se"]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/torrent/',),
                               ), callback='parse_tpb_torrent', follow=True),
        Rule(SgmlLinkExtractor(allow=(
                               '/browse/*/*/7',),), callback='tpb_category_org', follow=True),
        Rule(SgmlLinkExtractor(allow=('/browse/',),), callback='parse_tpb_category', follow=True))

            # in this one, we're not making any requests, just links
    def parse_tpb_category(self, response):
        slx = SgmlLinkExtractor(allow='/torrent/', deny=(
            '/img*', '/%0Ahttp://*'))
        sub_cats = slx.extract_links(response)
        for s in sub_cats:
            # print s
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

        page['title'] = hxs.select('//*[@id="title"]/text()').extract()[0]

        # layout with picture, like http://thepiratebay.se/torrent/8269933/

        page['seeds'] = hxs.select(
            '//*[@id="details"]/dl[1]/dd[7]/text()').extract()
        if page['seeds']:
            pass
        else:
            page['seeds'] = hxs.select(
                '//*[@id="details"]/dl[2]/dd[3]/text()').extract()

        if page['seeds'] != "":
            page['seeds'] = hxs.select(
                '//*[@id="details"]/dl[1]/dd[8]//text()').extract()

        # if there's 1 or less seeders, I don't care.
        # if eval(page['seeds']) <= 1:
        #	print'Not really seeded... discarded.'
        #	return None

        page['magnet'] = hxs.select(
            '//*[@id="details"]/div[3]/a[1]/@href').extract()
        if page['magnet']:
            pass
        else:
            page['magnet'] = hxs.select(
                '//*[@id="details"]/div[4]/a/@href').extract()
        # try it firefox's way too
        if page['magnet']:
            pass
        else:
            page['magnet'] = hxs.select(
                '/html/body/div[3]/div[2]/div/div/div/div[2]/div[10]/a/@href').extract()

        #//*[@id="details"]/div[3]/a
        #/html/body/table/tbody/tr[211]/td[2]/span[1]/a
        page['torrent'] = hxs.select(
            '//*[@id="details"]/div[4]/a[2]/@href').extract()
        if page['torrent']:
            pass
        else:
            page['torrent'] = hxs.select(
                '//*[@id="details"]/div[3]/a[2]/@href').extract()

        page['category'] = hxs.select(
            '//*[@id="details"]/dl[1]/dd[1]/a/text()').extract()
        # page['seeds']    =
        # hxs.select('//*[@id="details"]/dl[1]/dd[7]/text()').extract()

        # attempts the format with a picture first.
        page['leech'] = hxs.select(
            '//*[@id="details"]/dl[1]/dd[9]/text()').extract()
        if page['leech']:
            pass  # hxs.select('//*[@id="details"]/dl[1]/dd[8]/text()').extract()
        else:
            page['leech'] = hxs.select(
                '//*[@id="details"]/dl[2]/dd[4]/text()').extract()

        page['size'] = hxs.select(
            '//*[@id="details"]/dl[1]/dd[3]/text()').extract()
        # if page['size']: pass
        # else: page['size'] =

        page['added'] = hxs.select(
            '//*[@id="details"]/dl[1]/dd[5]/text()').extract()
        if page['added']:
            pass
        else:
            page['added'] = hxs.select(
                '//*[@id="details"]/dl[2]/dd[1]/text()').extract()

        page['uploader'] = hxs.select(
            '//*[@id="details"]/dl[1]/dd[6]/a/text()').extract()
        if page['uploader']:
            pass
        else:
            page['uploader'] = hxs.select(
                '//*[@id="details"]/dl[2]/dd[2]/a/text()').extract()

        # cleanup, removing excess data
        # if len(page['torrent']) > 1:
        #	del(page['torrent'][1])
        # del(page['added'][:2])
        # del(page['size' ][:2])

        return page

spider = PirateSpider()


@celery.task
def domain_crawl(domain_pk):
    spider.crawl(domain_pk)
