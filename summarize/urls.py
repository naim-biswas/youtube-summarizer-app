from django.urls import path
from .views import index, summarize

urlpatterns = [
    path('', index, name='index'),
    path('summarize/', summarize, name='summarize'),
]