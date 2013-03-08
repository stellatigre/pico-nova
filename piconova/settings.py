# Scrapy settings for piconova project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'piconova'
CONCURRENT_REQUESTS = 100
COOKIES_ENABLED = False
SPIDER_MODULES = ['piconova.spiders']
NEWSPIDER_MODULE = 'piconova.spiders'

#uas = 

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'piconova (+http://www.yourdomain.com)'
