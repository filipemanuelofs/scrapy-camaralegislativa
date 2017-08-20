# -*- coding: utf-8 -*-
import scrapy
from camaralegislativa.items import ViagemParlamentarItem


class ViagensSpider(scrapy.Spider):
    '''
    Classe responsável por gerenciar o crawler de viagens
    '''
    name = 'viagens'

    def start_requests(self):
        if not self.data_inicial and self.data_final:
            raise ValueError('Você precisa passar argumentos.')

        yield scrapy.Request(
            'http://www.camara.leg.br/missao-oficial/missao-pesquisa?deputado=1&nome-deputado=&nome-servidor=&dati={0}&datf={1}&nome-evento='.format(self.data_inicial, self.data_final)
        )

    def parse(self, response):
        '''
        Parse responsável pela extração inicial da página
        '''
        registros = response.xpath('//*[@id="content"]/div[2]/div/div/div/table/tbody[2]/tr')

        for registro in registros:
            viagem_parlamentar = ViagemParlamentarItem()
            url_relatorio = response.urljoin(
                registro.xpath('translate(normalize-space(./td[5]//tr[1]/td[2]/a/@href), " ","")').extract_first())

            viagem_parlamentar['inicio'] = registro.xpath('./td[1]/text()').extract_first()
            viagem_parlamentar['termino'] = registro.xpath('./td[2]/text()').extract_first()
            viagem_parlamentar['assunto'] = registro.xpath('./td[3]/text()').extract_first()
            viagem_parlamentar['destino'] = registro.xpath('./td[4]/text()').extract_first()
            viagem_parlamentar['deputado'] = registro.xpath('./td[5]//span/text()').extract_first()
            viagem_parlamentar['situacao_relatorio'] = registro.xpath(
                'normalize-space(./td[5]//tr[1]/td[2]/text())').extract_first()
            viagem_parlamentar['viagem_cancelada'] = registro.xpath('./td[6]/text()').extract_first()
            viagem_parlamentar['url_relatorio'] = response.urljoin(
                registro.xpath('translate(normalize-space(./td[5]//tr[1]/td[2]/a/@href), " ","")').extract_first())

            request = scrapy.Request(url_relatorio, callback=self.parse_detalhe_viagem)
            request.meta['item'] = viagem_parlamentar
            yield request

    def parse_detalhe_viagem(self, response):
        '''
        Parse responsável pelo detalhe da viagem do deputado
        '''
        viagem_parlamentar = response.meta['item']
        viagem_parlamentar['qnt_diarias'] = response.xpath(
            'substring-after(normalize-space(/*//li[contains(text(), "Quantidade")]/text()), ": ")').extract_first()
        viagem_parlamentar['valor'] = response.xpath(
            'substring-after(normalize-space(/*//li[contains(text(), "Valor")]/text()), ": ")').extract_first()
        viagem_parlamentar['tipo_passagem'] = response.xpath(
            'substring-after(normalize-space(/*//li[contains(text(), "Passagem")]/text()), ": ")').extract_first()
        yield viagem_parlamentar
