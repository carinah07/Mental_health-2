from rest_framework import serializers
from .models import ContentNode

class ContentNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentNode
        fields = ['id', 'title_en', 'title_sw', 'content_en', 'content_sw', 'parent', 'node_type']
