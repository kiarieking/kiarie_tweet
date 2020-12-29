from django.shortcuts import render, get_object_or_404,Http404,redirect
from django.http import HttpResponse, JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings
from .models import Tweet
import random
from .forms import Tweetform
# Create your views here.



ALLOWED_HOSTS = settings.ALLOWED_HOSTS
def home_view(request):
    print(request.user or none)
    return render(request, 'pages/home.html')


def tweet_create_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        user=None
        if request.is_ajax():
            return JsonResponse({},status=401)
        return redirect(settings.LOGIN_URL)

    form = Tweetform(request.POST or None)
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user or None
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        if next_url != None and is_safe_url(next_url,ALLOWED_HOSTS):
            return redirect(next_url)
        form = Tweetform()
    if form.errors:
        if request.is_ajax():
             return JsonResponse(form.errors,status=400)
    return render(request, 'components/form.html', context={'form':form} )

def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
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
        
