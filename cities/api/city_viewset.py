from rest_framework import viewsets

from cities.api.city_serializer import CitySerializer
from cities.models import City


class CityViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	API endpoint that allows cities to be viewed
	"""
	queryset = City.objects.all().order_by('name')
	serializer_class = CitySerializer
	permission_classes = ()
