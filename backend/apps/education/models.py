from django.db import models

class ContentNode(models.Model):
    NODE_TYPES = [
        ('user', 'User Education'),
        ('teacher', 'Teacher Training'),
        ('parent', 'Parent Training'),
    ]

    title_en = models.CharField(max_length=255)
    title_sw = models.CharField(max_length=255)
    content_en = models.TextField(blank=True, null=True)
    content_sw = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    node_type = models.CharField(max_length=20, choices=NODE_TYPES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_en
