from django.shortcuts import render, get_object_or_404,Http404,redirect
from django.http import HttpResponse, JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings
from .models import Tweet
import random
from .forms import Tweetform
from .serializer import TweetSerializer, TweetActionSerialier
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
# Create your views here.


ALLOWED_HOSTS = settings.ALLOWED_HOSTS
def home_view(request):
    print(request.user or none)
    return render(request, 'pages/home.html')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
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


@api_view(['DELETE','POST'])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
     qs = Tweet.objects.filter(id=tweet_id)
     if not qs.exists():
         return Response({}, status=404)
     qs = qs.filter(user=request.user)
     if not qs.exists():
         return Response({'message':'You cannot delete this tweet!'}, status=403)
     obj = qs.first()
     obj.delete()
     return Response({'message':'Tweet deleted'}, status=200)   



@api_view(['GET','POST'])
def tweet_like_view(request, tweet_id, *args, **kwargs):
    tweet = Tweet.objects.filter(id=tweet_id)
    user = request.user
    if tweet.exists() and user.is_authenticated:
        tweet.first().likes.add(user)
    else:
        return Response({'message':'You cannot like this tweet'}) 
    return Response('You liked that tweet.')  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    serializer = TweetActionSerialier(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        id = data.get('id')
        action = data.get('action')

        qs = Tweet.objects.filter(id = id)
        if not qs.exists():
            return Response({'message':'This tweet does not exist'}, status=404)
        obj = qs.first()
        if action == 'like':
            obj.likes.add(request.user)
        elif action == 'unlike':
            obj.likes.remove(request.user)
        elif action == 'retweet':
            pass           
    return Response({'message':'Tweet liked'}, status=200)
       

# def tweet_create_view_Django(request, *args, **kwargs):
#     user = request.user
#     if not user.is_authenticated:
#         user=None
#         if request.is_ajax():
#             return JsonResponse({},status=401)
#         return redirect(settings.LOGIN_URL)

#     form = Tweetform(request.POST or None)
#     next_url = request.POST.get('next') or None
#     if form.is_valid():
#         obj = form.save(commit=False)
#         obj.user = request.user or None
#         obj.save()
#         if request.is_ajax():
#             return JsonResponse(obj.serialize(), status=201)
#         if next_url != None and is_safe_url(next_url,ALLOWED_HOSTS):
#             return redirect(next_url)
#         form = Tweetform()
#     if form.errors:
#         if request.is_ajax():
#              return JsonResponse(form.errors,status=400)
#     return render(request, 'components/form.html', context={'form':form} )

# def tweet_list_view_pure_Django(request, *args, **kwargs):
#     qs = Tweet.objects.all()
#     tweets_list = [x.serialize() for x in qs]
#     data = {
#         "response":tweets_list
#     }
#     return JsonResponse(data)


# def tweet_detail_view_pure_Django(request,tweet_id, *args, **kwargs):
#     data = {"id":tweet_id}
#     try:
#         obj = Tweet.objects.get(id=tweet_id)
#         data["content"] = obj.content
#         status = 200
#     except:
#         data["message"] = "not found"
#         status = 404
#     return JsonResponse(data,status=status)
        
