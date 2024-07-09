from django.urls import path
from smartapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update/<int:form_id>/', views.update, name='dashboard'),
    path('logout/', views.logoutUser, name='logout'),  
    path('form/', views.form, name='form'),
    path('display/<int:form_id>/', views.display, name='display'),
    path('download/<int:form_id>/', views.generate_pdf, name='download'),
    path('download-excel/<int:form_id>/', views.generate_excel, name='download-excel'),
    path('export_excel/<int:form_id>/', views.export_excel, name='export_excel'),
]