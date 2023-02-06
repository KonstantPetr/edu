from django_filters import FilterSet, DateFilter, DateFromToRangeFilter
from .models import Post
from django import forms


class NewsFilter(FilterSet):
    creation_dt = DateFilter(widget=forms.DateInput(attrs={'type': 'date'}), lookup_expr='gt', label='Start date')

    class Meta:
        model = Post
        fields = {
            'author': ['exact'],
            'header': ['icontains'],
        }


class ArticlesFilter(NewsFilter, FilterSet):  # вдруг захочется какие-то особенности статей подчеркнуть
    pass  # думаю, на такой случай потенциально лучше иметь отдельный фильтр
