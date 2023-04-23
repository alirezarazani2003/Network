from urllib import response
from django.test import TestCase, Client
from django.db.models import Max

from .models import User, Posts, Follow


# Create your tests here.
class NetworkTEstCase(TestCase):

    def setUp(self):
        
        #Create User
        u1 = User.objects.create(username = "u1", email = "u1@gmail.com", password = "123456")
        u2 = User.objects.create(username = "u2", email = "u2@gmail.com", password = "123456")
        u3 = User.objects.create(username = "u3", email = "u3@gmail.com", password = "123456")

        #Create Post
        p1 = Posts.objects.create(user = u1, content = "Hello' World", likes = 1)
        p2 = Posts.objects.create(user = u1, content = "", likes = 1)
        p3 = Posts.objects.create(user = u1, content = "Hello' World", likes = -1)

        #Create Follow
        f1 = Follow.objects.create(user = u1)
        f1.following.add(u2)
        f1.follower.add(u2)

        
        f2 = Follow.objects.create(user = u2)
        f2.following.add(u2)
        f2.follower.add(u1)

        f3 = Follow.objects.create(user = u3)
        f3.following.add(u1)
        f3.follower.add(u3)

    #---Test-0--------------------------------------------------------------------------------
    def test_Post_creater_count(self):
        a = User.objects.get(username = "u1")
        self.assertEqual(a.user.count(), 3)
    #---Test-1--------------------------------------------------------------------------------
    def test_valid_Post(self):
        u1 = User.objects.get(username = "u1")
        p = Posts.objects.get(user = u1, content = "Hello' World", likes = 1)
        self.assertTrue(p.is_valid_Post())
    #---Test-2--------------------------------------------------------------------------------
    def test_invalid_Post_like(self):
        u1 = User.objects.get(username = "u1")
        p = Posts.objects.get(user = u1, content = "Hello' World", likes = -1)
        self.assertFalse(p.is_valid_Post())
    #---Test-3--------------------------------------------------------------------------------
    def test_invalid_Post_content(self):
        u1 = User.objects.get(username = "u1")
        p = Posts.objects.get(user = u1, content = "", likes = 1)
        self.assertFalse(p.is_valid_Post())
    #---Test-4--------------------------------------------------------------------------------
    def test_valid_Follow(self):
        u1 = User.objects.get(username = "u1")
        f = Follow.objects.get(user= u1)
        self.assertTrue(f.is_valid_follow())
    #---Test-5--------------------------------------------------------------------------------
    def test_invalid_Follow_following(self):
        u2 = User.objects.get(username = "u2")
        g = Follow.objects.get(user= u2)
        self.assertFalse(g.is_valid_follow())
    #---Test-6--------------------------------------------------------------------------------
    def test_invalid_Follow_follower(self):
        u3 = User.objects.get(username = "u3")
        g = Follow.objects.get(user= u3)
        self.assertFalse(g.is_valid_follow())
    #---Test-7--------------------------------------------------------------------------------
    def test_index(self):
        c = Client()
        response = c.get("")
        self.assertEqual(response.status_code, 200)
        self.assertEqual (response.context["Posts"].count(), 3)
    #---Test-8--------------------------------------------------------------------------------
    def test_following(self):
        max_id =  User.objects.all().aggregate(Max("id"))["id__max"]
        c = Client()
        response = c.get(f"/follow/{max_id + 1}")
        self.assertEqual(response.status_code, 404)
    #---Test-9--------------------------------------------------------------------------------
    def test_following(self):
        max_id =  User.objects.all().aggregate(Max("id"))["id__max"]
        c = Client()
        response = c.get(f"/unfollow/{max_id + 1}")
        self.assertEqual(response.status_code, 404)