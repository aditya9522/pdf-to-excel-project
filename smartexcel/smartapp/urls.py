from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Map /smartapp/ocrform/ to index view (form.html)
]