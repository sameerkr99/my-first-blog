from django.contrib import admin
# Register your models here.
from .models import Post, Categories, Profile,comments,Upvotes
admin.site.register(Post)
admin.site.register(Categories)
admin.site.register(Profile)
admin.site.register(comments)
admin.site.register(Upvotes)

