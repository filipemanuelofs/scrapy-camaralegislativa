# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ViagemParlamentarItem(scrapy.Item):
    inicio = scrapy.Field()
    termino = scrapy.Field()
    assunto = scrapy.Field()
    destino = scrapy.Field()
    deputado = scrapy.Field()
    url_relatorio = scrapy.Field()
    situacao_relatorio = scrapy.Field()
    viagem_cancelada = scrapy.Field()
    qnt_diarias = scrapy.Field()
    valor = scrapy.Field()
