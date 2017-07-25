# -*- coding: utf-8 -*-
import scrapy


class ViagensSpider(scrapy.Spider):
    name = 'viagens'
    allowed_domains = [
        'www.camara.leg.br/missao-oficial/missao-pesquisa?deputado=1&nome-deputado=&nome-servidor=&dati=01%2F06%2F2017&datf=30%2F06%2F2017&nome-evento='
    ]
    start_urls = [
        'http://www.camara.leg.br/missao-oficial/missao-pesquisa?deputado=1&nome-deputado=&nome-servidor=&dati=01%2F06%2F2017&datf=30%2F06%2F2017&nome-evento=/'
    ]

    def parse(self, response):
        titulo = response.xpath('//*[@id="content"]/h3/text()').extract_first()
        registros = response.xpath('//*[@id="content"]/div[2]/div/div/div/table/tbody[2]/tr')

        for registro in registros:
            inicio = registro.xpath('./td[1]/text()').extract_first()
            termino = registro.xpath('./td[2]/text()').extract_first()
            assunto = registro.xpath('./td[3]/text()').extract_first()
            destino = registro.xpath('./td[4]/text()').extract_first()
            deputado = registro.xpath('./td[5]//span/text()').extract_first()
            cancelada = registro.xpath('./td[6]/text()').extract_first()

            yield {
                'inicio': inicio,
                'termino': termino,
                'assunto': assunto,
                'destino': destino,
                'deputado': deputado,
                'cancelada': cancelada,
            }