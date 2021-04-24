from django.contrib import admin

# Register your models here.

from .models import Tweet, Follow

admin.site.register(Tweet)
admin.site.register(Follow)
