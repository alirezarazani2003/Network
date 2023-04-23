
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_post, name="create"),

 
    path("user/<int:username>", views.profile, name="profile"),
    path("follow/<int:username>", views.follow, name="follow"),
    path("unfollow/<int:user_id>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    
    path("edite", views.edite, name="edite"),
    path("like", views.like, name="like"),


]
