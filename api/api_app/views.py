from elasticsearch import Elasticsearch
from rest_framework.views import APIView
from rest_framework.response import Response

es = Elasticsearch(['http://localhost:9200'])


class StockListView(APIView):
    def get(self, request):
        query = {
            "query": {
                "match_all": {}
            }
        }

        response = es.search(index='stocks_data', body=query)

        hits = response['hits']['hits']

        stocks = []
        for hit in hits:
            stock_data = hit['_source']
            stocks.append(stock_data)

        return Response(stocks)


class StockDetailView(APIView):
    def get(self, request, pk):
        query = {
            "query": {
                "match": {
                    "id": pk
                }
            }
        }

        response = es.search(index='stocks_data', body=query)

        hits = response['hits']['hits']

        if hits:
            stock_data = hits[0]['_source']
            return Response(stock_data)
        else:
            return Response({'message': 'Stock not found'}, status=404)


class StockSearchView(APIView):
    def get(self, request):
        """
        Query Parameters:
        - search: The search query to match stock names.
        Example:
        /stocks/search/?search=Block
        """
        search_query = request.query_params.get('search')

        query = {
            "query": {
                "match": {
                    "stock_name": search_query
                }
            }
        }

        response = es.search(index='stocks_data', body=query)

        hits = response['hits']['hits']

        stocks = []
        for hit in hits:
            stock_data = hit['_source']
            stocks.append(stock_data)

        return Response(stocks)


class StockFilterView(APIView):
    def get(self, request):
        """
        Query Parameters:
        - min_price, max_price:  Specify the price range to filter.
        Example:
        /stocks/search/?price_min=50&price_max=100
        """
        min_price = float(request.query_params.get('price_min'))
        max_price = float(request.query_params.get('price_max'))

        query = {
            "query": {
                "range": {
                    "prev_close": {
                        "gte": min_price,
                        "lte": max_price
                    }
                }
            }
        }

        response = es.search(index='stocks_data', body=query)

        hits = response['hits']['hits']

        stocks = []
        for hit in hits:
            stock_data = hit['_source']
            stocks.append(stock_data)

        return Response(stocks)

