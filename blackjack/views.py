from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class ShowPageView(TemplateView):
    template_name = 'blackjack/index.html'
