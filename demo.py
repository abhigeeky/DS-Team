import scrapy
from scrapy.http import Response, Request

class BskincareSpider(scrapy.Spider):
    name = 'bskincare'
    allowed_domains = ['bskincaretx.com']
    start_urls = ['https://www.bskincaretx.com/shop']

    def parse(self, response):
        # Extract product links
        product_links = response.css('a.AJctir.bGFTjD::attr(href)').extract()
        product_links = [response.urljoin(link) for link in product_links]

        for link in product_links:
            yield scrapy.Request(link, callback=self.parse_product)

    def parse_product(self, response):
        # Extract product title
        title = response.css('div.FQirFG::text').get()
        # Extract product image URL
        image_url = response.css('img.sjzXVoa::attr(src)').get()
        # Extract product price
        price = response.css('div.hM4gpp div.pszKa5::text').get()
        yield {
            'title': title,
            'image_url': image_url,
            'price': price,
            'url': response.url
        }
    