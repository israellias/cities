from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from cities.models import City


class CityTestCase(TestCase):
	def setUp(self):
		City.objects.create(name='Bogotá', admin_name='Bogotá')
		City.objects.create(name='Medellín', admin_name='Antioquia')

	def test_city_fields(self):
		"""Animals that can speak are correctly identified"""
		bogota = City.objects.get(name='Bogotá')
		medellin = City.objects.get(name='Medellín')
		self.assertEqual(bogota.name, 'Bogotá')
		self.assertEqual(medellin.admin_name, 'Antioquia')
		medellin.delete()
		bogota.delete()

	def test_file_upload(self):
		file_content = f"""city,lat,lng,country,iso2,admin_name,capital,population,population_proper\n
		"Bogotá,4.6126,-74.0705,Colombia,CO,Bogotá,primary,9464000,7963000\n
		"Medellín,6.2447,-75.5748,Colombia,CO,Antioquia,admin,2529403,2529403"""
		file = SimpleUploadedFile(
			"test.csv",
			file_content.encode('utf-8')
		)
		response = self.client.post('/cities/upload/', {'file': file})
		data = response.json()
		self.assertEqual(data.get('loading'), 2)

		medellin = City.objects.filter(name='Medellín').exists()
		self.assertTrue(medellin)

	def test_search(self):
		file_content = f"""city,lat,lng,country,iso2,admin_name,capital,population,population_proper\n
		"Cali,4.6126,-74.0705,Colombia,CO,Antioquia,primary,9464000,7963000\n
		"Medellín,6.2447,-75.5748,Colombia,CO,Antioquia,,,"""
		file = SimpleUploadedFile(
			"test.csv",
			file_content.encode('utf-8')
		)
		self.client.post('/cities/upload/', {'file': file})

		response = self.client.get('/cities/search/', {'q': 'cali'})
		data = response.json()
		results = data.get('results')

		self.assertGreater(len(results), 0)
		self.assertEqual(results[0]['name'], 'Cali')
