from cities.models import City


def process_city(city):
	City.objects.update_or_create(
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
