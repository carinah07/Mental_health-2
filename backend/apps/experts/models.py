from django.db import models

class Expert(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    district = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.region}, {self.district})"
