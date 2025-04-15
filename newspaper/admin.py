from django.contrib import admin

from newspaper.models import Advertisement, Category, Post, Tag

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Advertisement)
