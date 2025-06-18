# pylint: skip-file
from decimal import Decimal

from pytest import fixture
from pandas import Timestamp

from app import app


@fixture(scope="module")
def get_test_client():
    return app.test_client()


@fixture(scope="module")
def example_response():
    return [{'earthquake_id': 501, 'magnitude': Decimal('4.4'), 'latitude': Decimal('-25.1751'), 'longitude': Decimal('179.7428'), 'time': Timestamp('2025-06-17 01:24:35.190000+0000', tz='UTC'), 'updated': Timestamp('2025-06-17 01:44:55.040000+0000', tz='UTC'), 'depth': Decimal('514.023'), 'url': 'https://earthquake.usgs.gov/earthquakes/eventpage/us6000qkqy', 'felt': 0, 'tsunami': False, 'cdi': Decimal('NaN'), 'mmi': Decimal('NaN'), 'nst': 38, 'sig': 298, 'net': 'us', 'dmin': Decimal('7.559'), 'alert': None, 'location_source': None, 'magnitude_type': 'Mb', 'state_name': 'Not in the USA', 'region_name': 'No Country'}, {'earthquake_id': 499, 'magnitude': Decimal('4.2'), 'latitude': Decimal('34.4738'), 'longitude': Decimal('140.1843'), 'time': Timestamp('2025-06-17 01:07:22.846000+0000', tz='UTC'), 'updated': Timestamp('2025-06-17 01:28:22.040000+0000', tz='UTC'), 'depth': Decimal('113.642'), 'url': 'https://earthquake.usgs.gov/earthquakes/eventpage/us6000qkqx', 'felt': 0, 'tsunami': False, 'cdi': Decimal('NaN'), 'mmi': Decimal('NaN'), 'nst': 26, 'sig': 271, 'net': 'us', 'dmin': Decimal('1.39'), 'alert': None, 'location_source': None, 'magnitude_type': 'Mb', 'state_name': 'Not in the USA', 'region_name': 'No Country'}, {'earthquake_id': 504, 'magnitude': Decimal('4.4'), 'latitude': Decimal('-23.9577'), 'longitude': Decimal('-66.6589'), 'time': Timestamp('2025-06-17 02:06:47.716000+0000', tz='UTC'), 'updated': Timestamp('2025-06-17 03:01:12.040000+0000', tz='UTC'), 'depth': Decimal('195.267'), 'url': 'https://earthquake.usgs.gov/earthquakes/eventpage/us6000qkr2', 'felt': 0, 'tsunami': False, 'cdi': Decimal('NaN'), 'mmi': Decimal('NaN'), 'nst': 26, 'sig': 298, 'net': 'us', 'dmin': Decimal('1.718'), 'alert': None, 'location_source': None, 'magnitude_type': 'Mb', 'state_name': 'Not in the USA', 'region_name': 'Argentina'}, {'earthquake_id': 503, 'magnitude': Decimal('4.8'), 'latitude': Decimal('-7.0902'), 'longitude': Decimal('155.6893'), 'time': Timestamp('2025-06-17 02:20:26.099000+0000', tz='UTC'), 'updated': Timestamp('2025-06-17 02:44:59.040000+0000', tz='UTC'), 'depth': Decimal('75.308'), 'url': 'https://earthquake.usgs.gov/earthquakes/eventpage/us6000qkr3', 'felt': 0, 'tsunami': False, 'cdi': Decimal('NaN'), 'mmi': Decimal('NaN'), 'nst': 55, 'sig': 354, 'net': 'us', 'dmin': Decimal('4.539'), 'alert': None, 'location_source': None, 'magnitude_type': 'Mb', 'state_name': 'Not in the USA', 'region_name': 'Solomon Islands'}, {'earthquake_id': 500, 'magnitude': Decimal('5'), 'latitude': Decimal('-0.8897'), 'longitude': Decimal('-78.1283'), 'time': Timestamp('2025-06-17 01:46:26.420000+0000', tz='UTC'), 'updated': Timestamp('2025-06-17 01:58:04.040000+0000', tz='UTC'), 'depth': Decimal('6.38'), 'url': 'https://earthquake.usgs.gov/earthquakes/eventpage/us6000qkr0', 'felt': 0, 'tsunami': False, 'cdi': Decimal('NaN'), 'mmi': Decimal('NaN'), 'nst': 56, 'sig': 385, 'net': 'us', 'dmin': Decimal('0.275'), 'alert': None, 'location_source': None, 'magnitude_type': 'Mb', 'state_name': 'Not in the USA', 'region_name': 'Ecuador'}]
