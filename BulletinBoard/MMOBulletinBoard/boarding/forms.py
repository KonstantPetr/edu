from django import forms
from .models import Post, Response
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from django_summernote.widgets import SummernoteWidget


class PostForm(forms.ModelForm):
    header = forms.CharField(min_length=10)
    content = forms.CharField(widget=SummernoteWidget)

    class Meta:
        model = Post
        fields = [
            'category',
            'header',
            'content',
                  ]


class ResponseForm(forms.ModelForm):
    text = forms.CharField(min_length=15)

    class Meta:
        model = Response
        fields = [
            'text',
                  ]


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
