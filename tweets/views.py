from django.shortcuts import render, get_object_or_404,Http404,redirect
from django.http import HttpResponse, JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings
from .models import Tweet
import random
from .forms import Tweetform
from .serializer import TweetSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.


ALLOWED_HOSTS = settings.ALLOWED_HOSTS
def home_view(request):
    print(request.user or none)
    return render(request, 'pages/home.html')


@api_view(['POST'])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetSerializer(data=request.POST or None)
    if serializer.is_valid():
        serializer.save(user = request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data, )    


@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data)

def tweet_create_view_Django(request, *args, **kwargs):
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

def tweet_list_view_pure_Django(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        "response":tweets_list
    }
    return JsonResponse(data)


def tweet_detail_view_pure_Django(request,tweet_id, *args, **kwargs):
    data = {"id":tweet_id}
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data["content"] = obj.content
        status = 200
    except:
        data["message"] = "not found"
        status = 404
    return JsonResponse(data,status=status)
        
