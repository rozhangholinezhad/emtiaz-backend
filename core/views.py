from django.shortcuts import render
from django.views.generic import TemplateView



# Create your views here.

class Home(TemplateView):
    template_name= "core/home.html"


class About_us(TemplateView):
    template_name = "core/about_us.html"