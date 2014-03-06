# Scrapy settings for piconova project
#http://doc.scrapy.org/topics/settings.html

BOT_NAME = 'piconova'
CONCURRENT_REQUESTS = 420
COOKIES_ENABLED = False
SPIDER_MODULES = ['piconova.spiders']
NEWSPIDER_MODULE = 'piconova.spiders'

DOWNLOADER_MIDDLEWARES = {'piconova.random_user_agent.RandomUserAgentMiddleware': 400,
                          'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,}

USER_AGENT_LIST = ('Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3',
				   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.2.153.1 Safari/525.19',#
				   'Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2',
				   'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
				   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
				   'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
				   'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US)',
				   'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0')
