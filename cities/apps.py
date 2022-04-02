import requests
from django.apps import AppConfig
from django.conf import settings


class CitiesConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'cities'

	def ready(self):
		"""
		Configures the index. if it is executed twice then just 400 response is received
		"""
		try:
			requests.put(f"{settings.ELASTICSEARCH_URL}/cities", json={
				"settings": {
					"analysis": {
						"analyzer": {
							"folding": {
								"tokenizer": "standard",
								"filter": ["lowercase", "asciifolding"]
							}
						}
					}
				},
				"mappings": {
					"properties": {
						"name": {
							"type": "text",
							"analyzer": "folding"
						},
						"admin_name": {
							"type": "text",
							"analyzer": "folding"
						}
					}
				}
			})
		except:
			pass
