from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Expert
from .serializers import ExpertSerializer
from django.db.models import Q

class RegionList(APIView):
    def get(self, request):
        regions = Expert.objects.values_list('region', flat=True).distinct()
        return Response({"regions": sorted(set(regions))})


class DistrictList(APIView):
    def get(self, request, region):
        districts = Expert.objects.filter(region=region).values_list('district', flat=True).distinct()
        return Response({"districts": sorted(set(districts))})


class ExpertSearch(APIView):
    def get(self, request):
        region = request.query_params.get('region')
        district = request.query_params.get('district')

        if not region or not district:
            return Response({"experts": []})

        district_experts = Expert.objects.filter(region=region, district=district)
        region_other_experts = Expert.objects.filter(region=region).exclude(district=district)

        district_serialized = ExpertSerializer(district_experts, many=True).data
        region_serialized = ExpertSerializer(region_other_experts, many=True).data

        return Response({"experts": district_serialized + region_serialized})
