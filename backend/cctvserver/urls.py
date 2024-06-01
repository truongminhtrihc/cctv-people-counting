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
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from api import views as apiviews
import os 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/camera/', apiviews.get_camera_data),
    path('api/camera/rename/', apiviews.change_camera_name),
    path('api/stream-url/', apiviews.get_stream_url),
    path('api/video/', apiviews.get_video_list),
    path('api/video/rename', apiviews.rename_video),
    path('api/video/delete', apiviews.delete_video),
    path('api/traffic/', apiviews.get_traffic_data),
    path('api/average-traffic/', apiviews.get_average_traffic_data),
    path('api/total-traffic/', apiviews.get_total_traffic_data),
    path('api/average-total-traffic/', apiviews.get_average_total_traffic_data),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#dir_path = os.path.dirname(os.path.realpath(__file__))[0:-10]
#subprocess.Popen(['python', dir_path + 'aiservices.py', dir_path, settings.MEDIA_ROOT], creationflags=subprocess.CREATE_NEW_CONSOLE)
