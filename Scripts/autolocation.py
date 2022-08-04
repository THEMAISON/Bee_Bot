from decimal import Decimal
from yandex_geocoder import Client

from configure import config

client = Client(config.get('yandex_api'))

coordinates = {
    'latitude': Decimal(0.1),
    'longitude': Decimal(0.1)
}

address = ''


def identify_location(place_name):
    location_data = client.coordinates(place_name + ', Севастополь')
    coordinates['longitude'] = location_data[0]
    coordinates['latitude'] = location_data[1]
    global address
    address = client.address(location_data[0], location_data[1])
