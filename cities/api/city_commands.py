import tablib
from django_q.tasks import async_task
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from cities.api import process_city


@api_view(['POST'])
def upload_cities(request: Request):
	file = request.FILES.get('file')
	cities = file.read().decode('utf-8')

	dataset = tablib.Dataset()
	dataset.load(cities, format='csv')
	for city in dataset.dict:
		async_task(process_city, city)

	return Response({'loading': len(dataset)})
