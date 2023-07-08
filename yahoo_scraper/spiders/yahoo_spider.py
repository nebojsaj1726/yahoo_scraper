import scrapy
from ..items import StockItem
from ..analysis import DataAnalyzer
from elasticsearch import Elasticsearch
import logging
import uuid


class YahooSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_logger = logging.getLogger('my-logger')

    name = 'yahoo'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.93 Safari/537.36'
    }
    result_list = []

    def start_requests(self):
        url = 'https://finance.yahoo.com/screener/predefined/growth_technology_stocks'
        yield scrapy.Request(url=url, callback=self.parse_symbols, headers=self.headers)

    def parse_symbols(self, response):
        data_analyzer = DataAnalyzer()
        stock_symbols = response.xpath('//*[@id="scr-res-table"]/div[1]/table/tbody//tr/td[1]/a').css(
            '::text').extract()
        for symbol in stock_symbols:
            url = f"https://finance.yahoo.com/quote/{symbol}"
            yield scrapy.Request(url, callback=self.parse_stock, headers=self.headers,
                                 meta={'data_analyzer': data_analyzer})

    def parse_stock(self, response):
        data_analyzer = response.meta['data_analyzer']
        item = StockItem()

        item['id'] = str(uuid.uuid4())
        item['stock_name'] = response.xpath('//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1').css(
            '::text').extract()
        item['intraday_price'] = response.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]').css(
            '::text').extract()
        item['prev_close'] = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]').css(
            '::text').extract()
        item['range_day'] = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[5]/td[2]').css(
            '::text').extract()
        item['range_52weeks'] = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[6]/td[2]').css(
            '::text').extract()

        data_analyzer.process_data(item)

        self.result_list.append(item)

    def closed(self, reason):
        try:
            es = Elasticsearch(['http://localhost:9200'])
            item_dicts = [dict(item) for item in self.result_list]
            bulk_data = []

            for item_dict in item_dicts:
                bulk_data.append({
                    "index": {
                        "_index": "stocks_data"
                    }
                })
                bulk_data.append(item_dict)

            es.bulk(index="stocks_data", body=bulk_data)
            self.custom_logger.info('Data successfully written to Elasticsearch')
        except Exception as e:
            self.custom_logger.error(f"An error occurred while interacting with Elasticsearch: {e}")
