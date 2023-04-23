from pyexpat import model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Posts(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user")
    content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    luser = models.ManyToManyField(User, related_name="luser")
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "like" : self.likes
        }

    def is_valid_Post(self):
        return self.likes >= 0 and len(self.content) >= 1


class Follow(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="userF")
    following = models.ManyToManyField(User, related_name="Following")
    follower = models.ManyToManyField(User, related_name="Follower")

    def __str__(self):
        return f"{self.user}----{self.follower}-----{self.following}"

    def is_valid_follow(self):

        for i in self.following.all():
            if i == self.user:
                return False
        for i in self.follower.all():
            if i == self.user:
                return False

        return True
