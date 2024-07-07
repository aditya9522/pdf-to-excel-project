from django.urls import path
from smartapp import views

urlpatterns = [
    path('', views.index, name='index'),  # Map /smartapp/ocrform/ to index view (form.html)
    path('form/', views.form, name='form'),
    path('display/<int:form_id>/', views.display, name='display'),
    path('download/<int:form_id>/', views.generate_pdf, name='download'),
    path('export_excel/', views.export_excel, name='export_excel'),
]