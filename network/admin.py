from django.contrib import admin
from .models import Posts, User, Follow

# Register your models here.
admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Follow)