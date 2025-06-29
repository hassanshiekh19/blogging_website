from django.urls import path
from .views import (
    home,
    post_detail,
    post_create,
    post_edit,
    post_delete,
    like_post  # ✅ include like_post here
)

urlpatterns = [
    path("", home, name="home"),
    path("post/<int:pk>/", post_detail, name="post_detail"),
    path("post/new/", post_create, name="post_create"),
    path("post/<int:pk>/edit/", post_edit, name="post_edit"),
    path("post/<int:pk>/delete/", post_delete, name="post_delete"),
    
    # ✅ ADD THIS LINE
    path("like/", like_post, name="like_post"),
]
