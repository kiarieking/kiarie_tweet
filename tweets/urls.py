from django.urls import path
from . import views
urlpatterns = [
    path('home', views.home_view, name='home'),
    path('detail/<int:tweet_id>', views.tweet_detail_view, name='detail'),
    path('tweets', views.tweet_list_view, name='tweets'),
    path('tweet-create', views.tweet_create_view, name='tweet-create'),
    path('delete/<int:tweet_id>', views.tweet_delete_view, name='tweet_delete'),
    path('like/<int:tweet_id>', views.tweet_like_view, name='like_tweet')
]