from django.contrib import admin

from newspaper.models import Advertisement, Category, Comment, Contact, Post, Tag, UserProfile

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Advertisement)
admin.site.register(Contact)
admin.site.register(UserProfile)
admin.site.register(Comment)
