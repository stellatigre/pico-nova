# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

class PiconovaPipeline(object):
    def process_item(self, item, spider):	
		for p in item:
			entry = item[p][0] 
			entry.encode('utf-8', 'ignore')
		return item
