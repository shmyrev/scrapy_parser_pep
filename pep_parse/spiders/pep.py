import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_pep = response.css(
            'section[id=numerical-index] tbody a::attr(href)'
        )
        for pep_link in all_pep:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        number, name = (
            response.css('h1.page-title::text').get().split(' – ', 1)
        )
        pep_data = {
            'number': number.split()[1],
            'name': name,
            'status': response.css('abbr::text').get(),
        }
        yield PepParseItem(pep_data)
