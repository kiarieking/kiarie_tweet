from django.shortcuts import render, get_object_or_404,Http404
from django.http import HttpResponse
from .models import Tweet
# Create your views here.
def home_view(request):
    return HttpResponse('<h1>Twitter clone<h1>')

def tweet_detail_view(request,tweet_id, *args, **kwargs):
    try:
        obj = Tweet.objects.get(id=tweet_id)
    except:
        raise Http404
        
