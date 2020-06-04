from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from django.conf import settings
from django.conf.urls.static import static
from main.serializers import CustomAuthToken
urlpatterns = [
    path('auth/', CustomAuthToken.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include('main.urls')),
 ]
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)