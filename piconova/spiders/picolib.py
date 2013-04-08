from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from items import Torrent

xpath_dict = {}


def try_xpaths(Torrent, xp_dict, response):
    hxs = HtmlXPathSelector(response)
    for field in xp_dict:
        for xp in xp_dict[field]:
            Torrent[field] = hxs.select(xp).extract()
            if Torrent[field]:
                break


def make_requests_from_url(url):
    return Request(url, dont_filter=False, meta={'start_url': url})


class PicoSpider(CrawlSpider):
    name = "picospider"

    # in this one, we're not making any requests, just links
    def parse_category(self, response):
        tlx = SgmlLinkExtractor(allow=self.tor_links, deny=self.deny_rules)
        torrents = tlx.extract_links(response)
        for t in torrents:
            req = make_requests_from_url(t.url)
            return req

    # make torrent page requests from subcategories
    def parse_subcategory(self, response):
        slx = SgmlLinkExtractor(allow=self.tor_links, deny=self.deny_rules)
        sub_list = slx.extract_links(response)
        for s in sub_list:
            r = make_requests_from_url(s.url)
            return r

    def parse_torrent(self, response):
        page = Torrent()
        try_xpaths(page, self.xpath_dict, response)
        return page
