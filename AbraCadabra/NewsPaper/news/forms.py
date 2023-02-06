from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class NewsForm(forms.ModelForm):
    header = forms.CharField(min_length=10)
    text = forms.CharField(min_length=50)

    class Meta:
        model = Post
        fields = [
            'author',
            'categories',
            'header',
            'text',
                  ]

        def clean(self):
            cleaned_data = super().clean()
            header = cleaned_data.get('header')
            text = cleaned_data.get('text')
            if header == text:
                raise ValidationError('Заголовок не должен быть идентичен тексту.')

            return cleaned_data


class ArticlesForm(NewsForm, forms.ModelForm):  # аналогично filters
    pass
