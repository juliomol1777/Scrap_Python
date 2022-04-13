import scrapy
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
#from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
#from items import Relatos
#from items import Relatos
#from bs4 import BeautifulSoup

class Relatos(Item):
    titulo = Field()
    autor = Field()
    categoria = Field()
    texto = Field()

class RelatosCrawler(CrawlSpider):
    name = 'relato'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        #'CLOSESPIDER_PAGECOUNT': 5
        # Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
    }

    # Utilizamos 2 dominios permitidos, ya que los articulos utilizan un dominio diferente
    allowed_domains = ['relato.com']
    #para la paginacion elegida uso estas 2
    #page_number = 2
    #ultima_page = 669
    #start_urls = ['https://www.relato.com/categoria/588?&page=1']
    

    #start_urls = ['https://www.relato.com/categoria/588']
    
    start_urls = []
    for i in range (1, 670):
        start_urls.append('https://www.relato.com/categoria/588?&page=' + str(i))

    #para la paginacion puede ser asi
    """
        Este arreglo lo podriamos armar dinamicamente, algo tipo:
        start_urls = []
        for i in range (1, 669):
          start_urls.append('https://www.relato.com/categoria/588?&page=' + str(i))
    quedarian 669 url asi  
    
    start_urls = [
        'https://www.relato.com/categoria/588?&page=1'#,
        #'https://www.relato.com/categoria/588?&page=2'
    ]
    """

    download_delay = 1

    # Tupla de reglas
    rules = (
        #Rule(  # REGLA #1 => HORIZONTALIDAD POR PAGINACION, uso esta si hay un patron en cada pag horizontal
            #LinkExtractor(
                #allow=r'/588?&page='
                # Patron en donde se utiliza "\d+", expresion que puede tomar el valor de cualquier combinacion de numeros
            #), follow=True),
        Rule(  # REGLA #2 => VERTICALIDAD AL DETALLE DE LOS PRODUCTOS
            LinkExtractor(
                allow=r'/relato/'
                #limitar el espectro de búsqueda
                #,restrict_xpaths = ['//div[@id="content"]'] 
                #pongo follow=False para que no siga los link a relatos del mismo autor 
                #en la barra lateral
            ), follow=False, callback='parse_items'),
    # Al entrar al detalle de los productos, se llama al callback con la respuesta al requerimiento
    )

    def parse_items(self, response):
        item = ItemLoader(Relatos(), response)
        item.add_xpath('titulo', '//div[@class="col-10 offset-1"]//h1//text()')
        item.add_xpath('autor', "//div[@class='col-3 d-none d-lg-block']//h3//a//text()")
        item.add_xpath('categoria', "//div[@class='col-10 offset-1']//h3//a//text()")
        
        parrafos = response.xpath("//div[@class='relato']//p")
        texto = ''
        for parrafo in parrafos:
            text = parrafo.xpath(
                ".//text()").get()
            #salto = ' \n '
            texto += str(text)
        item.add_value('texto', texto)
        
        # Utilizo Map Compose con funciones anonimas
        #item.add_xpath('texto', "//div[@class='relato']//p/text()", MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))
        yield item.load_item()

        #paginacion
        #no puedo usar paginacion aca porque cada pagina contiene links 
        # y parese_item extrae informacion de esas paginas que estan en esos link, no del link
        """
        next_page = 'https://www.relato.com/categoria/588?&page=' + str(RelatosCrawler.page_number)

        if RelatosCrawler.page_number <= RelatosCrawler.ultima_page:
            RelatosCrawler.page_number +=1
            yield response.follow(next_page, callback= self.parse_items)

        #otra manera
        next_page = response.xpath("//footer/div[@class='row justify-content-center']/a/@href").get()
        if next_page:
            abs_url = f"https://www.relato.com{next_page}"
            yield scrapy.Request(
                url = abs_url,
                callback = self.parse_items
            )
        """

# EJECUCION
# scrapy runspider extractRelato.py -o extractRelato.json -t json
#agrego en settings.py esto para no tener caracteres extraños en el json de salida
#FEED_EXPORT_ENCODING = 'utf-8'