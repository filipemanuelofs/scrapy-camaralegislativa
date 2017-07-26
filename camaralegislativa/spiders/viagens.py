# -*- coding: utf-8 -*-
import scrapy
import urlparse


class ViagensSpider(scrapy.Spider):
    name = 'viagens'
    allowed_domains = [
        'www.camara.leg.br'
    ]
    start_urls = [
        'http://www.camara.leg.br/missao-oficial/missao-pesquisa?deputado=1&nome-deputado=&nome-servidor=&dati={0}&datf={1}&nome-evento='.format('01/01/2017', '31/03/2017')
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
            viagemCancelada = registro.xpath('./td[6]/text()').extract_first()
            situacao = registro.xpath('normalize-space(./td[5]//tr[1]/td[2]/text())').extract_first()
            linkRelatorio = registro.xpath('normalize-space(./td[5]//tr[1]/td[2]/a/@href)').extract_first()

            yield {
                'titulo': titulo,
                'inicio': inicio,
                'termino': termino,
                'assunto': assunto,
                'destino': destino,
                'deputado': deputado,
                'viagemCancelada': viagemCancelada,
                'situacaoRegistro': {
                    'situacao': situacao,
                    'linkRelatorio': response.urljoin(linkRelatorio)
                }
            }