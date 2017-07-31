# -*- coding: utf-8 -*-
import scrapy
import urlparse


class ViagensSpider(scrapy.Spider):
    name = 'viagens'
    start_urls = [
        'http://www.camara.leg.br/missao-oficial/missao-pesquisa?deputado=1&nome-deputado=&nome-servidor=&dati={0}&datf={1}&nome-evento='.format('01/01/2017', '31/03/2017')
    ]

    def parse(self, response):
        registros = response.xpath('//*[@id="content"]/div[2]/div/div/div/table/tbody[2]/tr')

        for registro in registros:
            urlRelatorio = response.urljoin(registro.xpath('translate(normalize-space(./td[5]//tr[1]/td[2]/a/@href), " ","")').extract_first())
            yield {
                'titulo': response.xpath('//*[@id="content"]/h3/text()').extract_first(),
                'inicio': registro.xpath('./td[1]/text()').extract_first(),
                'termino': registro.xpath('./td[2]/text()').extract_first(),
                'assunto': registro.xpath('./td[3]/text()').extract_first(),
                'destino': registro.xpath('./td[4]/text()').extract_first(),
                'deputado': registro.xpath('./td[5]//span/text()').extract_first(),
                'viagemCancelada': registro.xpath('./td[6]/text()').extract_first(),
                'situacaoRegistro': {
                    'situacao': registro.xpath('normalize-space(./td[5]//tr[1]/td[2]/text())').extract_first(),
                    'linkRelatorio': urlRelatorio
                },
                'detalheViagem': {
                    'quantidade': scrapy.Request(url=urlRelatorio, callback=self.parse_detail),
                    'valor': ''
                }
            }
    
    def parse_detail(self, response):
        registros = response.xpath('//*[@id="content"]/div/div/div/div/div[2]/ul')
        
        for registro in registros:
            yield { 
                registro.xpath('./li[1]/text()').extract_first()
            }