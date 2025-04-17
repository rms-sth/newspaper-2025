from django.contrib import admin

from newspaper.models import Advertisement, Category, Contact, Post, Tag

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Advertisement)
admin.site.register(Contact)
