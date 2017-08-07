# -*- coding: utf-8 -*-
import scrapy
from camaralegislativa.items import ViagemParlamentarItem

class ViagensSpider(scrapy.Spider):
    name = 'viagens'
    start_urls = [
        'http://www.camara.leg.br/missao-oficial/missao-pesquisa?deputado=1&nome-deputado=&nome-servidor=&dati={0}&datf={1}&nome-evento='.format('01/01/2017', '31/03/2017')
    ]
    viagem_parlamentar = ViagemParlamentarItem()

    def parse(self, response):
        registros = response.xpath('//*[@id="content"]/div[2]/div/div/div/table/tbody[2]/tr')

        for registro in registros:
            url_relatorio = response.urljoin(registro.xpath('translate(normalize-space(./td[5]//tr[1]/td[2]/a/@href), " ","")').extract_first())

            self.viagem_parlamentar['inicio'] = registro.xpath('./td[1]/text()').extract_first()
            self.viagem_parlamentar['termino'] = registro.xpath('./td[2]/text()').extract_first()
            self.viagem_parlamentar['assunto'] = registro.xpath('./td[3]/text()').extract_first()
            self.viagem_parlamentar['destino'] = registro.xpath('./td[4]/text()').extract_first()
            self.viagem_parlamentar['deputado'] = registro.xpath('./td[5]//span/text()').extract_first()
            self.viagem_parlamentar['situacao_relatorio'] = registro.xpath(
                'normalize-space(./td[5]//tr[1]/td[2]/text())').extract_first()
            self.viagem_parlamentar['viagem_cancelada'] = registro.xpath('./td[6]/text()').extract_first()
            self.viagem_parlamentar['url_relatorio'] = url_relatorio

            yield scrapy.Request(url_relatorio, callback=self.parse_detail)

    def parse_detail(self, response):
        registros = response.xpath('//*[@id="content"]/div/div/div/div/div[2]/ul')
        for registro in registros:
            self.viagem_parlamentar['qnt_diarias'] = registro.xpath('normalize-space(./li[1]/text())').extract_first()
            self.viagem_parlamentar['valor'] = registro.xpath('normalize-space(./li[2]/text())').extract_first()
            
            yield self.viagem_parlamentar
