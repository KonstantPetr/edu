from django_filters import FilterSet, DateFilter, DateFromToRangeFilter, ModelChoiceFilter
from .models import Post, Response
from django import forms


class PostFilter(FilterSet):
    cre_dt = DateFilter(widget=forms.DateInput(attrs={'type': 'date'}), lookup_expr='gt', label='Start date')

    class Meta:
        model = Post
        fields = {
            'header': ['icontains'],
        }


class ResponseFilter(FilterSet):

    post = ModelChoiceFilter(
        queryset=Post.objects.none(),
        label='Объявление',
        method='filter_post',
        empty_label='все'
    )

    class Meta:
        model = Response
        fields = {
            'post': ['exact'],
            'text': ['icontains'],
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.queryset = Response.objects.filter(post__sender=user)
        self.filters['post'].queryset = Post.objects.filter(sender=user)

    def filter_post(self, queryset, name, value):
        return queryset.filter(post=value)
