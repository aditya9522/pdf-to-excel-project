from django.urls import path
from . import views
from smartapp.views import display

urlpatterns = [
    path('ocrform/', views.index, name='index'),  # Map /smartapp/ocrform/ to index view (form.html)
    path('ocrform/display/', views.display, name='display'),
    path('ocrform/display/pdf/', views.generate_pdf, name='generate_pdf'),
]