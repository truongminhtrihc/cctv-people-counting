from django.contrib import admin
from api.models import Camera, Metadata, DailyTotal

class CameraAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status", "type", "video_ip", "camera_ip")

class MetadataAdmin(admin.ModelAdmin):
    list_display = ("camera", "hour", "date", "people_in", "people_out")

class DailyTotalAdmin(admin.ModelAdmin):
    list_display = ("camera", "date", "people_in", "people_out")

admin.site.register(Camera, CameraAdmin)
admin.site.register(Metadata, MetadataAdmin)
admin.site.register(DailyTotal, DailyTotalAdmin)