import scrapy
import Quandl
import settings_local


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
        "languages": ["<list-of-official/national-languages"],
        "population": "<population>",
        "density": "<people-per-square-km>",
        "_code": "<id-for-world-bank",
        "inet_users": 0,
        "control_of_corruption": 0,
        "life_expectancy_male": 0,
        "life_expectancy_female": 0,
        "population_growth": 0,
        "urban_population": 0,
        "surface_area": 0,
        "forest_area": 0,
        "military_expenditure": 0,
        "pc_per_100": 0,
        "infant_deaths": 0,
        "roads_total_network": 0,
        "vehicles_per_km_of_road": 0
    }
    ```
    """
    
    name = "Countries"

    start_urls = ('https://en.wikipedia.org/wiki/List_of_countries_by_Human_Development_Index',)
    world_bank_url = 'https://www.quandl.com/resources/api-for-country-data'

    def _get_abs_url(self, path):
        return "%s%s" % ("https://en.wikipedia.org", path)

    def parse(self, response):
        countries = []
        for row in response.xpath("//span[@id='Very_high_human_development']/../following-sibling::table[1]/tr/td/table/tr[position()>2]"):
            country = dict(
                position=int(row.xpath("td[1]/text()").extract()[0]),
                hdi=float(row.xpath("td[4]/text()").extract()[0]),
                name=row.xpath("td[3]/a[1]/text()").extract()[0],
                flag_small=row.xpath("td[3]/span/img[1]/@src").extract()[0],
                wiki=self._get_abs_url(row.xpath("td[3]/a[1]/@href").extract()[0])
            )
            countries.append(country)
            yield scrapy.Request(self.world_bank_url, callback=self.parse_world_bank_code, meta=dict(countries=countries))

    def parse_world_bank_code(self, response):
            base_xpath = response.xpath("//h2[@id='Countries-with-Statistical-Data']/following-sibling::table/tbody")
            for country in response.meta['countries']:
                if country['name'] == 'United Kingdom':
                    country['_code'] = 'GBR'
                elif country['name'] == 'Liechtenstein':
                    country['_code'] = 'LIE'
                elif country['name'] == 'Andorra':
                    country['_code'] = 'AND'
                elif country['name'] == 'Slovakia':
                    country['_code'] = 'SVK'
                elif country['name'] == 'United Arab Emirates':
                    country['_code'] = 'ARE'
                elif country['name'] == 'Korea, South':
                    country['_code'] = 'KOR'
                else:
                    country['_code'] = base_xpath.xpath("descendant::td[contains(text(), '%s')]/preceding-sibling::td/text()" % country['name']).extract()[0]
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
        # Population total
        self._parse_quandl(country, 'population', 'WORLDBANK/%s_SP_POP_TOTL')
        # Population density (peoples per km)
        self._parse_quandl(country, 'density', 'WORLDBANK/%s_EN_POP_DNST')
        # Count of internet users
        self._parse_quandl(country, 'inet_users', 'WORLDBANK/%s_IT_NET_USER')
        # Control of corruption (estimate), bigger is better
        self._parse_quandl(country, 'control_of_corruption', 'WORLDBANK/%s_CC_EST')
        # Life expectancy (male), in year
        self._parse_quandl(country, 'life_expectancy_male', 'WORLDBANK/%s_SP_DYN_LE00_MA_IN')
        # Life expectancy (female), in years
        self._parse_quandl(country, 'life_expectancy_female', 'WORLDBANK/%s_SP_DYN_LE00_FE_IN')
        # Population growth in percents
        self._parse_quandl(country, 'population_growth', 'WORLDBANK/%s_SP_POP_GROW')
        # Urban population (% of total)
        self._parse_quandl(country, 'urban_population', 'WORLDBANK/%s_SP_URB_TOTL_IN_ZS')
        # Surface area (sq. km) 
        self._parse_quandl(country, 'surface_area', 'WORLDBANK/%s_AG_SRF_TOTL_K2')
        # Forest area (sq. km)
        self._parse_quandl(country, 'forest_area', 'WORLDBANK/%s_AG_LND_FRST_K2')
        # Military expenditure
        self._parse_quandl(country, 'military_expenditure', 'WORLDBANK/%s_MS_MIL_XPND_CN')
        # Personal computers (per 100 people)
        self._parse_quandl(country, 'pc_per_100', 'WORLDBANK/%s_IT_CMP_PCMP_P2')
        # Number of infant deaths
        self._parse_quandl(country, 'infant_deaths', 'WORLDBANK/%s_SH_DTH_IMRT')
        # Roads, total network (km)
        self._parse_quandl(country, 'roads_total_network', 'WORLDBANK/%s_IS_ROD_TOTL_KM')
        # Vehicles (per km of road)
        self._parse_quandl(country, 'vehicles_per_km_of_road', 'WORLDBANK/%s_IS_VEH_ROAD_K1')
        return country

    def _parse_quandl(self, country, key, source_pattern):
        """ Get country parameter from Quandl """
        source = source_pattern % country['_code']
        try:
            res = Quandl.get(source, authroken=settings_local.QUANDL_TOKEN, rows=1)
        except Quandl.DatasetNotFound:
            country[key] = None
        else:
            country[key] = res.to_dict()['Value'].values()[0]
