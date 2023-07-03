import django_filters
from .models import Produit, Categorie

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Produit
        fields = ['nom_article']

class CategoryFilter(django_filters.FilterSet):
    class Meta: 
        model = Categorie
        fields = ['name']
