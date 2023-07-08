import scrapy


class StockItem(scrapy.Item):
    id = scrapy.Field()
    stock_name = scrapy.Field()
    intraday_price = scrapy.Field()
    prev_close = scrapy.Field()
    range_day = scrapy.Field()
    range_52weeks = scrapy.Field()
    data_summary = scrapy.Field()
    mean_intraday_price_change = scrapy.Field()
    max_intraday_price_change = scrapy.Field()
    min_intraday_price_change = scrapy.Field()
    daily_price_range = scrapy.Field()
    lowest_price = scrapy.Field()
    highest_price = scrapy.Field()
    year_lowest_price = scrapy.Field()
    year_highest_price = scrapy.Field()
