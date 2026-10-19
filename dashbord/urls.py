from django.urls import path

from .views import DashboardHomeView, DashboardProfileView

app_name = "dashbord"

urlpatterns = [
    path("", DashboardHomeView.as_view(), name="home"),
    path("profile/", DashboardProfileView.as_view(), name="profile"),
]
