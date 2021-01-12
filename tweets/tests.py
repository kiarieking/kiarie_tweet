from django.test import TestCase
from .models import Tweet
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
# Create your tests here.

User = get_user_model()
class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='king', password="password")
        tweet = Tweet.objects.create(id=1, content="Test tweet", user=self.user )
        tweet2 = Tweet.objects.create(content="Tweet 2 test", user = self.user)

    
    def get_client(self):
        client = APIClient()
        client.login(username = self.user.username, password = 'password')
        return client

    def test_tweetList(self):
        client = self.get_client()
        response = client.get('/tweets')
        self.assertEqual(response.status_code, 200)

    def test_api_tweetAction(self):
        client = self.get_client()
        response = client.post("/tweet_like/action",{"id":2, "action":"like"})
        self.assertEqual(response.status_code, 200)
        response = client.post("/tweet_like/action",{"id":2, "action":"unlike"}) 
        self.assertEqual(response.status_code, 200)
        response = client.post("/tweet_like/action", {"id":2, "action":"retweet"})
        self.assertEqual(response.status_code, 200)

    def test_tweetCreate(self):
        client = self.get_client()
        response = client.post("/tweet-create", {"content":"test tweet 7", "user":self.user})
        print (response.status_code)
        self.assertEqual(response.status_code, 201)    


        