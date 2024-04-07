"""
URL configuration for cctvserver project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import subprocess
from time import sleep
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from report import views as rpviews
from aiservice import views as aisviews
import os 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('report/camera/', rpviews.camera),
    path('report/traffic_by_time/', rpviews.traffic_by_time),
    path('report/most_least_traffic/', rpviews.most_least_traffic),
    path('aiservice/stream/', aisviews.stream),
    path('aiservice/stream_url/', aisviews.stream_url),
    path('aiservice/metadata/', aisviews.metadata),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


dir_path = os.path.dirname(os.path.realpath(__file__))[0:-10]
subprocess.Popen(['python', dir_path + 'aiservices.py', dir_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
