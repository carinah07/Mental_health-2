from django.urls import path
from . import views

urlpatterns = [
    path('content/roots/', views.list_root_nodes),
    path('content/<int:pk>/children/', views.list_child_nodes),
    path('content/<int:pk>/', views.get_node_details),
]
