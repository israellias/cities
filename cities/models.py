from django.db import models

from base.models import NULLABLE


class City(models.Model):
	# attributes
	name = models.CharField(max_length=255, unique=True, **NULLABLE)
	lat = models.DecimalField(max_digits=20, decimal_places=6, **NULLABLE)
	lng = models.DecimalField(max_digits=20, decimal_places=6, **NULLABLE)
	country = models.CharField(max_length=255, **NULLABLE)
	iso2 = models.CharField(max_length=2, **NULLABLE)
	admin_name = models.CharField(max_length=255, **NULLABLE)
	capital = models.CharField(max_length=255, **NULLABLE)
	population = models.IntegerField(**NULLABLE)
	population_proper = models.IntegerField(**NULLABLE)

	def __str__(self):
		return self.name
