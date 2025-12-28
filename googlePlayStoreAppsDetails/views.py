from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg
from .models import App, Review
from .serializers import AppSerializer, ReviewSerializer
from .forms import AppForm
from django.shortcuts import redirect

# main page 
def main_page(request):
	"""
	returns the main page of the app
	"""
	return render(request, 'index.html')


def top_rated_page(request):
    """
	Render a simple page that shows the top rated apps  
    """
    apps = App.objects.exclude(rating__isnull=True).order_by('-rating')[:50]
    return render(request, 'top_rated.html', {'apps': apps})
