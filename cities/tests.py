from django.test import TestCase

from cities.models import City


class AnimalTestCase(TestCase):
	def setUp(self):
		City.objects.create(name='Bogotá', admin_name='Bogotá')
		City.objects.create(name='Medellín', admin_name='Antioquia')

	def test_animals_can_speak(self):
		"""Animals that can speak are correctly identified"""
		bogota = City.objects.get(name='Bogotá')
		medellin = City.objects.get(name='Medellín')
		self.assertEqual(bogota.name, 'Bogotá')
		self.assertEqual(medellin.admin_name, 'Antioquia')
