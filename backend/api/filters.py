import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):

    # title =django_filters.CharFilter(lookup_expr='icontains')

    # publisher_name = django_filters.CharFilter(field_name='publisher__name', lookup_expr='icontains')

    # published_year_gte = django_filters.NumberFilter(field_name='published_year',lookup_expr='year__gte')

    # price_gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    # price_gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    # price_lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    # price_lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    # price = django_filters.NumberFilter(field_name='price', lookup_expr='exact')
    class Meta:
        model=Book
        fields ={
            'title':['icontains'],
            'publisher__name':['icontains'],
            'published_year':['exact','lt','lte','gt','gte'],
            'price':['exact','lt','lte','gt','gte']
            
        }
