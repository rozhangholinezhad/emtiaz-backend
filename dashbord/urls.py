from django.urls import path

from .views import (
    DashboardCategoryCreateView,
    DashboardCategoryDeleteView,
    DashboardCategoryListView,
    DashboardHomeView,
    DashboardPostCreateView,
    DashboardPostDeleteView,
    DashboardPostListView,
    DashboardPostUpdateView,
    DashboardProfileView,
)

app_name = "dashbord"

urlpatterns = [
    path("", DashboardHomeView.as_view(), name="home"),
    path("profile/", DashboardProfileView.as_view(), name="profile"),
    path("blog/", DashboardPostListView.as_view(), name="blog_list"),
    path("blog/new/", DashboardPostCreateView.as_view(), name="blog_create"),
    path("blog/<int:pk>/edit/", DashboardPostUpdateView.as_view(), name="blog_update"),
    path("blog/<int:pk>/delete/", DashboardPostDeleteView.as_view(), name="blog_delete"),
    path("categories/", DashboardCategoryListView.as_view(), name="category_list"),
    path("categories/new/", DashboardCategoryCreateView.as_view(), name="category_create"),
    path("categories/<int:pk>/delete/", DashboardCategoryDeleteView.as_view(), name="category_delete"),
]
