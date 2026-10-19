from django.urls import path
from .views import home, About_us

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('about-us/', About_us.as_view(), name='about'),
]