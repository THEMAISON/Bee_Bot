from yandex_geocoder import Client
from configure import config
from decimal import Decimal

client = Client(config.get('yandex_api'))

coordinates = {
    'latitude': Decimal(0.1),
    'longitude': Decimal(0.1)
}


def identify_location(place_name) -> None:
    location_data = client.coordinates(place_name)
    coordinates['longitude'] = location_data[0]
    coordinates['latitude'] = location_data[1]
