from django.urls import path
from .views import (
                  IndexView, MNewsList, SNewsDetail, NewsCreate, NewsUpdate, NewsDelete,
                  ArticlesList, ArticleDetail, ArticleCreate, ArticleUpdate, ArticleDelete,
                  CategoryList, CategoriesList, initiate_me, subscribe, unsubscribe,
                  )


urlpatterns = [
    path('', IndexView.as_view()),
    path('news/', MNewsList.as_view(), name='news_list'),
    path('news/<int:pk>', SNewsDetail.as_view(), name='news_detail'),
    path('news/create', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/update', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete', NewsDelete.as_view(), name='news_delete'),
    path('articles/', ArticlesList.as_view(), name='articles_list'),
    path('articles/<int:pk>', ArticleDetail.as_view(), name='article_detail'),
    path('articles/create', ArticleCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/update', ArticleUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete', ArticleDelete.as_view(), name='article_delete'),
    path('author_initiation/', initiate_me, name='author_initiation'),
    path('categories/<int:pk>', CategoryList.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
    path('categories/', CategoriesList.as_view(), name='categories_list'),
]
