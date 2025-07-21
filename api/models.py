from django.db import models

class Geoloc(models.Model):
    date = models.DateField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    type = models.TextField()
