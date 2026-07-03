from django.contrib import admin
from .models import ContentNode

@admin.register(ContentNode)
class ChatbotContentNodeAdmin(admin.ModelAdmin):
    list_display = ("title_en", "node_type", "level", "parent")
    list_filter = ("node_type",)
    search_fields = ("title_en", "title_sw")
