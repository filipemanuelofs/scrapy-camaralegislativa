# -*- coding: utf-8 -*-
from collections import Counter

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CamaralegislativaPipeline(object):
    destinos = []
    valores = []
    
    def process_item(self, item, spider):
        self.destinos.append(item['destino'])

        if item['valor'].isdigit():
            self.valores.append(float(item['valor']))

        return item

    def close_spider(self, spider):
        spider.logger.info(Counter(self.destinos).most_common())
        spider.logger.info(sum(v for v in self.valores))
