from django.urls import path
from .views import Home, About_us

app_name = 'core'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about-us/', About_us.as_view(), name='about'),
]