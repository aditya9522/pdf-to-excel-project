from django.urls import path
from smartapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('bulk-pdf', views.bulkPDF, name='bulk-pdf'),
    path('bulk-excel', views.bulkExcel, name='bulk-excel'),
    path('update/<int:stp_id>/', views.update, name='update'),
    path('logout/', views.logoutUser, name='logout'),  
    path('form/', views.form, name='form'),
    path('display/<int:stp_id>/', views.display, name='display'),
    path('download/<int:stp_id>/', views.generate_pdf, name='download'),
    path('download-excel/<int:stp_id>/', views.generate_excel, name='download-excel'),
    path('export-excel/<int:stp_id>/', views.export_excel, name='export-excel'),
]