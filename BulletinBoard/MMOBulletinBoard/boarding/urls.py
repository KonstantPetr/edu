from django.urls import path
from .views import (
                  IndexView, PostsList, PostCreate, PostUpdate, PostDelete,
                  ResponsesList, ResponseCreate, response_apply, response_deny
                  )

urlpatterns = [
    path('', IndexView.as_view()),
    path('posts/', PostsList.as_view(), name='posts_list'),
    path('posts/create', PostCreate.as_view(), name='post_create'),
    path('posts/<int:pk>/update', PostUpdate.as_view(), name='post_update'),
    path('posts/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('posts/<int:pk>/response', ResponseCreate.as_view(), name='response_create'),
    path('responses/', ResponsesList.as_view(), name='responses_list'),
    path('responses/<int:pk>/apply', response_apply, name='response_apply'),
    path('responses/<int:pk>/deny', response_deny, name='response_deny'),
]
