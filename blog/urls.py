from django.urls import path

from .views import PostCreateView, PostDetailView, PostListView, PostUpdateView

app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("new/", PostCreateView.as_view(), name="post_create"),
    path("<slug:slug>/edit/", PostUpdateView.as_view(), name="post_update"),
    path("<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
]
