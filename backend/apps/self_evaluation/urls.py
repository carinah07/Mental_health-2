from django.urls import path
from .views import phq9_assessment, gad7_assessment, update_followup_details, update_followup_details_child, child_assessment

urlpatterns = [
    path('phq9/', phq9_assessment, name='phq9'),
    path('gad7/', gad7_assessment, name='gad7'),
    path('sdq/', child_assessment, name='sdq'),
    path('followup/<int:pk>/', update_followup_details, name='update_followup'),
    path('followup/child/<int:pk>/', update_followup_details_child, name='update_followup_child'),
]

