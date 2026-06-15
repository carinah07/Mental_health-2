from django.db import models

# Create your models here.
class ContentNode(models.Model):
    title_en = models.CharField(max_length=255)
    title_sw = models.CharField(max_length=255)
    node_type = models.CharField(max_length=50)
    level = models.IntegerField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    content_en = models.TextField(blank=True)
    content_sw = models.TextField(blank=True)
