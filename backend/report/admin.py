from django.contrib import admin
from report.models import Camera, Metadata

class CameraAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status", "ip")

class MetadataAdmin(admin.ModelAdmin):
    list_display = ("camera", "time", "people_in", "people_out")

admin.site.register(Camera, CameraAdmin)
admin.site.register(Metadata, MetadataAdmin)