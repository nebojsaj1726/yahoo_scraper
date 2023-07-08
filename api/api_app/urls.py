from django.urls import path
from . import views

urlpatterns = [
    path('stocks/', views.StockListView.as_view(), name='stock-list'),
    path('stocks/<uuid:pk>/', views.StockDetailView.as_view(), name='stock-detail'),
    path('stocks/search/', views.StockSearchView.as_view(), name='stock-search'),
    path('stocks/filter/', views.StockFilterView.as_view(), name='stock-filter'),
]
