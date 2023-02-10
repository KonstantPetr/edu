from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


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


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
