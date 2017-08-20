# scrapy-camaralegislativa
---
Utilização do Scrapy para algumas páginas da Câmara Legislativa.

## Pré-requisito
- Python 2.7 ou acima
- Scrapy 1.4

### Teste
[Viagens em Missão Oficial](http://www.camara.leg.br/missao-oficial/index.jsp)
```
scrapy crawl viagens -a data_inicial=01/06/2017 -a data_final=30/06/2017
```
O resultado será escrito no arquivo ```viagens.json```.

### Argumentos
| Argumento    | Descrição                   |
|--------------|-----------------------------|
| data_inicial | Período inicial da consulta |
| data_final   | Período final da consulta   |