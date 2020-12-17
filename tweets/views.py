from django.shortcuts import render, get_object_or_404,Http404,redirect
from django.http import HttpResponse, JsonResponse
from .models import Tweet
import random
from .forms import Tweetform
# Create your views here.
def home_view(request):
    return render(request, 'pages/home.html')


def tweet_create_view(request, *args, **kwargs):
    form = Tweetform(request.POST or None)
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if next_url != None:
            return redirect(next_url)
        form = Tweetform()
    return render(request, 'components/form.html', context={'form':form} )

def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [{"id":x.id, "content":x.content, "likes":random.randint(0,1001)}for x in qs]
    data = {
        "response":tweets_list
    }
    return JsonResponse(data)


def tweet_detail_view(request,tweet_id, *args, **kwargs):
    data = {"id":tweet_id}
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data["content"] = obj.content
        status = 200
    except:
        data["message"] = "not found"
        status = 404
    return JsonResponse(data,status=status)
        
