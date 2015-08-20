import scrapy


class CountriesSpider(scrapy.Spider):

    """
    Get top `count` countries by Human Development Index in json:

    ```json
    {
        "position": "<HDI-position>",
        "hdi": "<HDI-value>",
        "name": "<country-name>",
        "flag_small": "<small-flag-image-url>",
        "flag_big": "<big-flag-image-url>",
        "iso_code": "<iso-code>",
        "wiki": "<country-wikipedia-page-url>",
        "map": "<country-on-map-url>",
        "languages": ["<list-of-official/national-languages"]
    }
    ```
    """
    
    name = "Countries"

    start_urls = ('https://en.wikipedia.org/wiki/List_of_countries_by_Human_Development_Index',)

    def _get_abs_url(self, path):
        return "%s%s" % ("https://en.wikipedia.org", path)

    def parse(self, response):
        results = []
        for row in response.xpath("//span[@id='Very_high_human_development']/../following-sibling::table[1]/tr/td/table/tr[position()>2]"):
            country = dict(
                position=int(row.xpath("td[1]/text()").extract()[0]),
                hdi=float(row.xpath("td[4]/text()").extract()[0]),
                name=row.xpath("td[3]/a[1]/text()").extract()[0],
                flag_small=row.xpath("td[3]/span/img[1]/@src").extract()[0],
                wiki=self._get_abs_url(row.xpath("td[3]/a[1]/@href").extract()[0])
            )
            yield scrapy.Request(country['wiki'], callback=self.parse_country, meta=dict(country=country))


    def parse_country(self, response):
        country = response.meta['country']
        country['iso_code'] = response.xpath("//a[@title='ISO 3166']/../following-sibling::td/a/text()").extract()[0]
        country['flag_big'] = response.xpath("//table[contains(@class, 'geography')]/descendant::img/@src").extract()[0]
        country['map'] = response.xpath("//table[contains(@class, 'geography')]/descendant::div[@class='floatnone'][descendant::img]/a/img/@src").extract()[0]
        # National languages
        if country['name'] in ('Australia', 'United States', 'Japan'):
            lang_base = response.xpath("//th/descendant-or-self::*[contains(text(),'National language')]/ancestor-or-self::th/following-sibling::td")
        else:
        # Official languages
            lang_base = response.xpath("//th/descendant-or-self::*[contains(text(),'Official language')]/ancestor-or-self::th/following-sibling::td")
        languages = lang_base.xpath("span/a/text()").extract() + \
                lang_base.xpath("a/text()").extract() + \
                lang_base.xpath("div[@class='plainlist']/descendant::a[not(ancestor::sup)]/text()").extract() + \
                lang_base.xpath("div[@class='hlist']/descendant::li[not(descendant::a)]/text()").extract() + \
                lang_base.xpath("div[@class='hlist']/descendant::a[not(ancestor::sup)]/text()").extract() + \
                lang_base.xpath("self::td[not(child::*)]/text()").extract()
        country['languages'] = languages
        return country
