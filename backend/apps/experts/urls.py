from django.urls import path
from .views import RegionList, DistrictList, ExpertSearch

urlpatterns = [
    path('regions/', RegionList.as_view(), name='region-list'),
    path('regions/<str:region>/districts/', DistrictList.as_view(), name='district-list'),
    path('search/', ExpertSearch.as_view(), name='expert-search'),
]
