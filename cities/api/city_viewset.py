from collections import OrderedDict

import requests
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from cities.api.city_serializer import CitySerializer
from cities.models import City


class CityViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	API endpoint that allows cities to be viewed
	"""
	queryset = City.objects.all().order_by('name')
	serializer_class = CitySerializer
	permission_classes = ()

	@action(methods=['GET'], detail=False)
	def search(self, request: Request, *args, **kwargs):
		query = request.query_params.get('q')

		res = requests.get(f"{settings.ELASTICSEARCH_URL}/cities/_search", json={
			"query": {
				"simple_query_string": {
					"query": f"*{query}*",
					"fields": ["name", "admin_name"],
					"default_operator": "and",
					"analyze_wildcard": True
				}
			}
		})

		hits = res.json().get('hits').get('hits')
		return Response(OrderedDict([
			('results', [{**h['_source']} for h in hits])
		]))
