from django.contrib import admin
from .models import Post, Comment, Category, Tag 

admin.site.register(Post) # i have Registered the Post model
admin.site.register(Comment) # i have Registered the Comment model
admin.site.register(Category)  # 👈 Register Category
admin.site.register(Tag)     