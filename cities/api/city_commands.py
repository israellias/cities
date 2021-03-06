import requests
import tablib
from django.conf import settings
from django_q.tasks import async_task
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from cities.api.city_serializer import CitySerializer
from cities.models import City


def _store_on_db(city):
	return City.objects.update_or_create(
		name=city.get('city'),
		defaults={
			'name': city['city'],
			'lat': city.get('lat') or None,
			'lng': city.get('lng') or None,
			'country': city.get('country'),
			'iso2': city.get('iso2'),
			'admin_name': city.get('admin_name'),
			'capital': city.get('capital'),
			'population': city.get('population') or None,
			'population_proper': city.get('population_proper') or None,
		}
	)


def _store_on_elasticsearch(obj):
	serializer = CitySerializer(obj)
	res = requests.put(
		f"{settings.ELASTICSEARCH_URL}/cities/_doc/{obj.pk}",
		json=serializer.data
	)
	print(f"{res.json().get('_id')} added")


def process_city(city):
	obj, _ = _store_on_db(city)
	_store_on_elasticsearch(obj)


@api_view(['POST'])
def upload_cities(request: Request):
	file = request.FILES.get('file')
	cities = file.read().decode('utf-8')

	dataset = tablib.Dataset()
	dataset.load(cities, format='csv')
	for city in dataset.dict:
		async_task(process_city, city)

	return Response({'loading': len(dataset)})
