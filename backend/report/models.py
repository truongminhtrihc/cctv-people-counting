from django.db import models

class Camera(models.Model):
    CAMERA_STATUS = [
        ("ON","On"),
        ("OFF","Off"),
        ("DIS","Disconnected")
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="Camera")
    status = models.CharField(max_length=3, choices=CAMERA_STATUS, default="OFF")
    ip = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Metadata(models.Model):
    id = models.BigAutoField(primary_key=True)
    camera = models.ForeignKey(to=Camera, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    people_in = models.PositiveBigIntegerField()
    people_out = models.PositiveBigIntegerField()

    class Meta:
        ordering = ['camera', '-time']
        indexes = [
            models.Index(fields=["camera", "-time"])
        ]
    
    def __str__(self):
        return str(self.camera) + " " + str(self.time) + " " + str(self.people_in) + " " + str(self.people_out)

