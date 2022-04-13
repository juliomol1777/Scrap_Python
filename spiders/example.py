import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['relato.com']
    start_urls = ['https://www.relato.com/relato/427787']
    #patron [0-9] es 0123456789

    def parse(self, response):
        #Dentro de la clase  col-10 offset-1 del div extraigo el texto dentro de h1
        titulo = response.xpath("//div[@class='col-10 offset-1']//h1//text()").extract_first()
        autor = response.xpath("//div[@class='col-3 d-none d-lg-block']//h3//a//text()").extract_first()
        categoria = response.xpath("//div[@class='col-10 offset-1']//h3//a//text()").extract_first()
        #Dentro de la clase relato del div, elijo los p y como son varios hago un for, luego los uno con acumulador texto
        parrafos = response.xpath("//div[@class='relato']//p")
        texto = ''
        for parrafo in parrafos:
            text = parrafo.xpath(
                ".//text()").extract_first()
            salto = ' \n '
            texto = texto + salto + text
        yield {'titulo': titulo, 'categoria': categoria, 'autor': autor, 'texto': texto}
