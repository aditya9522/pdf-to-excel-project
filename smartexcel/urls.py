from django.contrib import admin
from django.urls import include, path
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static
from smartapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('smartapp.urls')),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'smartapp.views.custom_404' 
handler500 = 'smartapp.views.custom_500' 