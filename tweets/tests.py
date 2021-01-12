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

        # like button
        response = client.post("/tweet_like/action",{"id":2, "action":"like"})
        self.assertEqual(response.status_code, 200)
        likes_count = response.json().get('likes')
        self.assertEqual(likes_count,1)

        # unlike button
        response = client.post("/tweet_like/action",{"id":2, "action":"unlike"}) 
        self.assertEqual(response.status_code, 200)
        likes_count = response.json().get("likes")
        self.assertEqual(likes_count, 0)

        # retweet button
        response = client.post("/tweet_like/action", {"id":2, "action":"retweet"})
        self.assertEqual(response.status_code, 201)
        new_tweet_id = response.json().get("id")
        self.assertNotEqual(new_tweet_id, 2)

    def test_tweetCreate(self):
        client = self.get_client()
        response = client.post("/tweet-create", {"content":"test tweet 7", "user":self.user})
        self.assertEqual(response.status_code, 201)    

    def test_tweetDetail(self):
        client = self.get_client()
        response = client.get("/detail/2")
        self.assertEqual(response.status_code, 200)
        print (len(response.json()))
        # self.assertEqual(len(response.json()), 1)
        