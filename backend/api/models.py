from django.db import models

class Camera(models.Model):
    CAMERA_STATUS = [
        ("ON","On"),
        ("OFF","Off"),
        ("DIS","Disconnected")
    ]
    CAMERA_TYPES = [
        ("AREA", "Area camera"),
        ("ENTR", "Entrance camera")
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="Camera")
    status = models.CharField(max_length=3, choices=CAMERA_STATUS, default="OFF")
    type = models.CharField(max_length=4, choices=CAMERA_TYPES, default="AREA")
    video_ip = models.CharField(max_length=50)
    camera_ip = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Metadata(models.Model):
    id = models.BigAutoField(primary_key=True)
    camera = models.ForeignKey(to=Camera, on_delete=models.CASCADE)
    hour = models.IntegerField()
    date = models.DateField()
    people_in = models.PositiveBigIntegerField()
    people_out = models.PositiveBigIntegerField()

    class Meta:
        ordering = ['-hour', '-date', 'camera']
        #indexes = []
    
    def __str__(self):
        return str(self.camera) + " " + str(self.date) + " " + str(self.hour) + " " + str(self.people_in) + " " + str(self.people_out)
    
class DailyTotal(models.Model):
    id = models.BigAutoField(primary_key=True)
    camera = models.ForeignKey(to=Camera, on_delete=models.CASCADE)
    date = models.DateField()
    people_in = models.PositiveBigIntegerField()
    people_out = models.PositiveBigIntegerField()

    class Meta:
        ordering = ['-date', 'camera']
        #indexes = []
    
    def __str__(self):
        return str(self.camera) + " " + str(self.date) + " " + str(self.people_in) + " " + str(self.people_out)

