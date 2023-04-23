from ast import Delete
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from .models import Posts, Follow, User
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

#----------------------------------------------------------------------------------

def index(request):
    posts = Posts.objects.all()
    posts = posts.order_by("-timestamp").all()
    
    page_num = request.GET.get('page')

    posts_paginator = Paginator(posts, 10) 
    page = posts_paginator.get_page(page_num)
    

    return render(request, "network/index.html",{
        "page" : page , "Posts":posts
    })

#----------------------------------------------------------------------------------

@csrf_exempt
@login_required
def edite(request):
    if request.method == "POST":
        data = json.loads(request.body)
        body = data.get("body", "")
        id = data.get("id", "")
        F = Posts.objects.get(pk = id)
        F.content = body
        F.save()
    return JsonResponse({"S": "Email sent successfully."}, status=201)

#----------------------------------------------------------------------------------

@csrf_exempt
@login_required
def like(request):
    if request.method == "POST":

        data = json.loads(request.body)
        id = data.get("id", "")
        if  Posts.objects.filter(luser = request.user, id = id).exists():
                act = Posts.objects.get(pk = id)
                attendee = User.objects.get(pk = request.user.id)
                act.luser.remove(attendee)
                
                m = Posts.objects.get(pk = id)
                m.likes -=1
                m.save()
                return render(request, "network/index.html",{
                    "x" :0
                })
        else:
            p = get_object_or_404(User, id = request.user.id)
            user_list, created = Posts.objects.get_or_create(pk = id)
            user_list.luser.add(p)

            m = Posts.objects.get(pk = id)
            m.likes +=1
            m.save()
            return render(request, "network/index.html",{
                "x" :1
            })
    return render(request, "network/index.html")

#----------------------------------------------------------------------------------
@login_required
def unfollow(request,user_id):
    attendee = get_object_or_404(User, id = user_id)
    act = Follow.objects.get(user = request.user)

    act.following.remove(attendee)

    u = request.user.id
    act1 = Follow.objects.get(user = user_id)
    attendee1 = User.objects.get(pk = u)
    act1.follower.remove(attendee1)
    return HttpResponseRedirect(reverse('profile', args=[user_id]))
#----------------------------------------------------------------------------------

def profile(request,username):
    posts = Posts.objects.filter(user = username)
    posts = posts.order_by("-timestamp").all()

    u = User.objects.get(id = username)
    usernam = u.username

    id = username
    if Follow.objects.filter(user = username).exists():
        user = Follow.objects.get(user = username)
        x = user.follower.count()
        y = user.following.count()
    else:
        x = 0
        y = 0
    if request.user.is_authenticated:
        if  Follow.objects.filter(user = request.user, following = username).exists():
            co = 0
        elif request.user.id == username:
            co = 2
        else : co = 1
    else: co = 3
    return render(request, "network/profile.html",{
        "Posts" : posts, "ID" : id, "X":x, "Y":y, "Co":co, "username":usernam
    })

#----------------------------------------------------------------------------------
@login_required
def following(request):

    F = Follow.objects.get(user = request.user)
    U = F.following.all()
    G = Posts.objects.filter(user__in = U)
    G = G.order_by("-timestamp").all()

    page_num = request.GET.get('page')

    posts_paginator = Paginator(G, 15) 
    page = posts_paginator.get_page(page_num)
    return render(request, "network/following.html",{
        "page": page, "Posts":G
    })

#----------------------------------------------------------------------------------
@login_required
def follow(request,username):
    user = get_object_or_404(User, id = username)
    user_list, created = Follow.objects.get_or_create(user=request.user)
    user_list.following.add(user)

    user1 = get_object_or_404(User, id = request.user.id)
    u = User.objects.get(id = username)
    user_list, created = Follow.objects.get_or_create(user=u)
    user_list.follower.add(user1)
    return HttpResponseRedirect(reverse('profile', args=[username]))

#----------------------------------------------------------------------------------
@login_required
def create_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            User = request.user
            Content = request.POST["content"]


           
            post = Posts()
            post.user = User
            post.content = Content
            post.save()
            return HttpResponseRedirect(reverse("index"))

        else : return render(request, "network/index.html")

    else : return render(request, "network/login.html")
    
#----------------------------------------------------------------------------------

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

#----------------------------------------------------------------------------------

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

#----------------------------------------------------------------------------------

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

#----------------------------------------------------------------------------------