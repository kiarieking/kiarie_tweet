from django.urls import path
from . import views
urlpatterns = [
    path('home', views.home_view, name='home'),
    path('detail/<int:tweet_id>', views.tweet_detail_view, name='detail'),
    path('tweets', views.tweet_list_view, name='tweets'),
    path('tweet-create', views.tweet_create_view, name='tweet-create')
]