import numpy as np
import pandas as pd
import re
import logging


class DataAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger('my-logger')

    def process_data(self, item):
        df = pd.DataFrame(item.items())

        for index, row in df.iterrows():
            key = row[0]
            values = row[1]

            if key == 'stock_name':
                item['stock_name'] = values[0]
            elif key == 'intraday_price':
                if len(values):
                    intraday_prices = []
                    for price in values:
                        numeric_price = re.search(r'(-?\d+(?:\.\d+)?)', price)
                        if numeric_price:
                            intraday_prices.append(float(numeric_price.group()))
                    if intraday_prices:
                        item['mean_intraday_price_change'] = round(float(np.mean(intraday_prices)), 2)
                        item['max_intraday_price_change'] = np.max(intraday_prices)
                        item['min_intraday_price_change'] = np.min(intraday_prices)
                else:
                    self.logger.info('No intraday prices available')
            elif key == 'prev_close':
                if len(values):
                    item['prev_close'] = float(values[0])
                else:
                    self.logger.info('No previous close price available')
            elif key == 'range_day':
                if len(values):
                    range_day = values[0]
                    low, high = map(float, range_day.split(' - '))
                    item['range_day'] = range_day
                    item['lowest_price'] = low
                    item['highest_price'] = high
                else:
                    self.logger.info('No daily price range available')
            elif key == 'range_52weeks':
                if len(values):
                    range_52weeks = values[0]
                    low, high = map(float, range_52weeks.split(' - '))
                    item['range_52weeks'] = range_52weeks
                    item['year_lowest_price'] = low
                    item['year_highest_price'] = high
                else:
                    self.logger.info('No 52 weeks price range available')

        data_summary = df.describe().to_dict()
        item['data_summary'] = data_summary

        return item
