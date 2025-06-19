# pylint: skip-file

"""Fixtures for tests in this directory."""

from json import loads
from pandas import DataFrame
from pytest import fixture
from datetime import datetime
from pytz import timezone
from unittest.mock import MagicMock


@fixture
def example_detailed_event():
    """An example of a detailed USGS API response."""
    return loads("""{"type": "Feature","properties":{"mag":0.53,"place":"10 km SSW of Idyllwild, CA","time":1749655031680,"updated":1749675581157,"tz":null,"url":"https://earthquake.usgs.gov/earthquakes/eventpage/ci41182664","felt":null,"cdi":null,"mmi":null,"alert":null,"status":"reviewed","tsunami":0,"sig":4,"net":"ci","code":"41182664","ids":",ci41182664,","sources":",ci,","types":",nearby-cities,origin,phase-data,scitech-link,","nst":15,"dmin":0.06854,"rms":0.13,"gap":115,"magType":"ml","type":"earthquake","title":"M 0.5 - 10 km SSW of Idyllwild, CA","products":{"nearby-cities":[{"indexid":5431596,"indexTime":1749675579811,"id":"urn:usgs-product:ci:nearby-cities:ci41182664:1749675578440","type":"nearby-cities","code":"ci41182664","source":"ci","updateTime":1749675578440,"status":"UPDATE","properties":{"eventsource":"ci","eventsourcecode":"41182664","pdl-client-version":"Version 2.7.10 2021-06-21"},"preferredWeight":7,"contents":{"nearby-cities.json":{"contentType":"application/json","lastModified":1749675578000,"length":596,"url":"https://earthquake.usgs.gov/realtime/product/nearby-cities/ci41182664/ci/1749675578440/nearby-cities.json"}}}],"origin":[{"indexid":5431595,"indexTime":1749675578850,"id":"urn:usgs-product:ci:origin:ci41182664:1749675577830","type":"origin","code":"ci41182664","source":"ci","updateTime":1749675577830,"status":"UPDATE","properties":{"azimuthal-gap":"115","depth":"15.81","depth-type":"from location","error-ellipse-azimuth":"357","error-ellipse-intermediate":"768","error-ellipse-major":"1248","error-ellipse-minor":"552","error-ellipse-plunge":"75","error-ellipse-rotation":"10","evaluation-status":"final","event-type":"earthquake","eventParametersPublicID":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?eventid=41182664","eventsource":"ci","eventsourcecode":"41182664","eventtime":"2025-06-11T15:17:11.680Z","horizontal-error":"0.31","latitude":"33.6663333","longitude":"-116.771","magnitude":"0.53","magnitude-azimuthal-gap":"123.5","magnitude-error":"0.206","magnitude-num-stations-used":"7","magnitude-source":"CI","magnitude-type":"ml","minimum-distance":"0.06854","num-phases-used":"28","num-stations-used":"15","origin-source":"CI","pdl-client-version":"Version 2.7.10 2021-06-21","quakeml-magnitude-publicid":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?magnitudeid=109412373","quakeml-origin-publicid":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?originid=105898557","quakeml-publicid":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?eventid=41182664","review-status":"reviewed","standard-error":"0.13","title":"10 km SSW of Idyllwild, CA","version":"6","vertical-error":"0.51"},"preferredWeight":157,"contents":{"contents.xml":{"contentType":"application/xml","lastModified":1749675578000,"length":195,"url":"https://earthquake.usgs.gov/realtime/product/origin/ci41182664/ci/1749675577830/contents.xml"},"quakeml.xml":{"contentType":"application/xml","lastModified":1749675577000,"length":3423,"url":"https://earthquake.usgs.gov/realtime/product/origin/ci41182664/ci/1749675577830/quakeml.xml"}}}],"phase-data":[{"indexid":5431597,"indexTime":1749675580880,"id":"urn:usgs-product:ci:phase-data:ci41182664:1749675577830","type":"phase-data","code":"ci41182664","source":"ci","updateTime":1749675577830,"status":"UPDATE","properties":{"azimuthal-gap":"115","depth":"15.81","depth-type":"from location","error-ellipse-azimuth":"357","error-ellipse-intermediate":"768","error-ellipse-major":"1248","error-ellipse-minor":"552","error-ellipse-plunge":"75","error-ellipse-rotation":"10","evaluation-status":"final","event-type":"earthquake","eventParametersPublicID":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?eventid=41182664","eventsource":"ci","eventsourcecode":"41182664","eventtime":"2025-06-11T15:17:11.680Z","horizontal-error":"0.31","latitude":"33.6663333","longitude":"-116.771","magnitude":"0.53","magnitude-azimuthal-gap":"123.5","magnitude-error":"0.206","magnitude-num-stations-used":"7","magnitude-source":"CI","magnitude-type":"ml","minimum-distance":"0.06854","num-phases-used":"28","num-stations-used":"15","origin-source":"CI","pdl-client-version":"Version 2.7.10 2021-06-21","quakeml-magnitude-publicid":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?magnitudeid=109412373","quakeml-origin-publicid":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?originid=105898557","quakeml-publicid":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?eventid=41182664","review-status":"reviewed","standard-error":"0.13","title":"10 km SSW of Idyllwild, CA","version":"6","vertical-error":"0.51"},"preferredWeight":157,"contents":{"contents.xml":{"contentType":"application/xml","lastModified":1749675578000,"length":195,"url":"https://earthquake.usgs.gov/realtime/product/phase-data/ci41182664/ci/1749675577830/contents.xml"},"quakeml.xml":{"contentType":"application/xml","lastModified":1749675577000,"length":100216,"url":"https://earthquake.usgs.gov/realtime/product/phase-data/ci41182664/ci/1749675577830/quakeml.xml"}}}],"scitech-link":[{"indexid":5431598,"indexTime":1749675582101,"id":"urn:usgs-product:ci:scitech-link:ci41182664-waveform_ci:1749675581157","type":"scitech-link","code":"ci41182664-waveform_ci","source":"ci","updateTime":1749675581157,"status":"UPDATE","properties":{"addon-code":"Waveform_CI","addon-type":"LinkURL","eventsource":"ci","eventsourcecode":"41182664","pdl-client-version":"Version 2.7.10 2021-06-21","text":"Waveforms","url":"https://scedc.caltech.edu/review_eventfiles/makePublicView.html?evid=41182664","version":"01"},"preferredWeight":7,"contents":[]}]}},"geometry":{"type":"Point","coordinates":[-116.771,33.6663333,15.81]},"id":"ci41182664"}""")


@fixture
def expected_columns():
    """List of columns expected from sql query to database."""
    return [
        "earthquake_id`", "magnitude", "time", "updated", "longitude", "latitude",
        "depth", "url", "tsunami", "felt", "cdi", "mmi", "nst",
        "sig", "net", "dmin", "alert", "location_source",
        "magnitude_type", "state_name", "region_name"
    ]


@fixture
def mock_conn():
    """Empty connection object."""
    return MagicMock()


@fixture
def example_dict():
    """Example record in database."""
    return {
        "earthquake_id": 1, "magnitude": 2.5, "latitude": 10.0, "longitude": 20.0,
        "time": "2024-01-01", "updated": "2024-01-02", "depth": 5.0, "url": "example.com",
        "felt": 1, "tsunami": 0, "cdi": None, "mmi": None, "nst": None,
        "sig": None, "net": None, "dmin": None, "alert": None,
        "location_source": None, "magnitude_type": None,
        "state_name": "California", "region_name": "West Coast",
        "state_id": 12, "region_id": 4
    }


@fixture
def example_df():
    """Example dataframe with two earthquake entries."""
    return DataFrame([
        {
            "earthquake_id": 1, "magnitude": 2.5, "latitude": 10.0, "longitude": 20.0,
            "time": 1749753475, "updated": 1749753475, "depth": 5.0, "url": "example.com",
            "felt": 1, "tsunami": 0, "cdi": 3.1, "mmi": 2.3, "nst": 1,
            "sig": 1, "net": "us", "dmin": 0.1, "alert": "green",
            "location_source": "us", "magnitude_type": "mb",
            "state_name": "California", "region_name": "West Coast"
        },
        {
            "earthquake_id": 2, "magnitude": 4.0, "latitude": 11.0, "longitude": 21.0,
            "time": 1749753475, "updated": 1749753475, "depth": 10.0, "url": "another.com",
            "felt": 2, "tsunami": 1, "cdi": 3.0, "mmi": 2.5, "nst": 5,
            "sig": 100, "net": "us", "dmin": 0.1, "alert": "green",
            "location_source": "us", "magnitude_type": "mb",
            "state_name": "Nevada", "region_name": "West Coast"
        }
    ])


@fixture
def example_df2():
    """Second example dataframe with one duplicate entry from example_df."""
    london_tz = timezone("Europe/London")
    return DataFrame([
        {
            "earthquake_id": 1, "magnitude": 2.5, "latitude": 10.0, "longitude": 20.0,
            "time": london_tz.localize(datetime.fromtimestamp(1749753475/1000)),
            "updated": london_tz.localize(datetime.fromtimestamp(1749753475/1000)),
            "depth": 5.0, "url": "example.com",
            "felt": 1, "tsunami": 0, "cdi": 3.1, "mmi": 2.3, "nst": 1,
            "sig": 1, "net": "us", "dmin": 0.1, "alert": "green",
            "location_source": "us", "magnitude_type": "mb",
            "state_name": "California", "region_name": "West Coast",
            "state_id": 12, "region_id": 4
        }
    ])


@fixture
def example_diff():
    """Expected difference between example_df and example_df2 (only the unique row)."""
    london_tz = timezone("Europe/London")
    return DataFrame([
        {
            "magnitude": 4.0, "latitude": 11.0, "longitude": 21.0,
            "time": london_tz.localize(datetime.fromtimestamp(1749753475/1000)),
            "updated": london_tz.localize(datetime.fromtimestamp(1749753475/1000)),
            "depth": 10.0, "url": "another.com",
            "felt": 2, "tsunami": True, "cdi": 3.0, "mmi": 2.5, "nst": 5,
            "sig": 100, "net": "us", "dmin": 0.1, "alert": "green",
            "magnitude_type": "Mb", "state_name": "Nevada",
            "region_name": "West Coast"
        }
    ])


@fixture
def example_topic():
    """Expected topic arn containing dictionary."""
    return DataFrame([
        {
            "topic_arn": "arn:aws:sns:eu-west-2:129033205317:c17-quake-4-12-22-100",
            "magnitude": 4.0, "latitude": 11.0, "longitude": 21.0,
            "time": "2024-02-01", "felt": 2, "tsunami": 1,
            "state_name": "Nevada", "region_name": "West Coast"
        }
    ])


@fixture
def example_earthquake_api_response():
    """Expected response from earthquake API."""
    return {'type': 'FeatureCollection', 'metadata': {'generated': 1750339085000, 'url': 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2025-06-19T12%3A18%3A05&endtime=2025-06-19T14%3A18%3A05&eventtype=earthquake', 'title': 'USGS Earthquakes', 'status': 200, 'api': '1.14.1', 'count': 8}, 'features': [{'type': 'Feature', 'properties': {'mag': 1.68, 'place': '9 km NNE of Pinnacles, CA', 'time': 1750338953120, 'updated': 1750339050445, 'tz': None, 'url': 'https://earthquake.usgs.gov/earthquakes/eventpage/nc75197686', 'detail': 'https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=nc75197686&format=geojson', 'felt': None, 'cdi': None, 'mmi': None, 'alert': None, 'status': 'automatic', 'tsunami': 0, 'sig': 43, 'net': 'nc', 'code': '75197686', 'ids': ',nc75197686,', 'sources': ',nc,', 'types': ',nearby-cities,origin,phase-data,', 'nst': 17, 'dmin': 0.05878, 'rms': 0.28, 'gap': 67, 'magType': 'md', 'type': 'earthquake', 'title': 'M 1.7 - 9 km NNE of Pinnacles, CA'}, 'geometry': {'type': 'Point', 'coordinates': [-121.122329711914, 36.6069984436035, 5.30000019073486]}, 'id': 'nc75197686'}, {'type': 'Feature', 'properties': {'mag': 1.09, 'place': '7 km ESE of Scofield, Utah', 'time': 1750337122280, 'updated': 1750339012460, 'tz': None, 'url': 'https://earthquake.usgs.gov/earthquakes/eventpage/uu80110581', 'detail': 'https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=uu80110581&format=geojson', 'felt': None, 'cdi': None, 'mmi': None, 'alert': None, 'status': 'reviewed', 'tsunami': 0, 'sig': 18, 'net': 'uu', 'code': '80110581', 'ids': ',uu80110581,', 'sources': ',uu,', 'types': ',origin,phase-data,', 'nst': 9, 'dmin': 0.1126, 'rms': 0.08, 'gap': 165, 'magType': 'ml', 'type': 'earthquake', 'title': 'M 1.1 - 7 km ESE of Scofield, Utah'}, 'geometry': {'type': 'Point', 'coordinates': [-111.075833333333, 39.6943333333333, 7.44]}, 'id': 'uu80110581'}, {'type': 'Feature', 'properties': {'mag': 1.62, 'place': '1 km ENE of The Geysers, CA', 'time': 1750336592420, 'updated': 1750338736048, 'tz': None, 'url': 'https://earthquake.usgs.gov/earthquakes/eventpage/nc75197676', 'detail': 'https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=nc75197676&format=geojson', 'felt': None, 'cdi': None, 'mmi': None, 'alert': None, 'status': 'automatic', 'tsunami': 0, 'sig': 40, 'net': 'nc', 'code': '75197676', 'ids': ',nc75197676,', 'sources': ',nc,', 'types': ',nearby-cities,origin,phase-data,scitech-link,', 'nst': 28, 'dmin': 0.00675, 'rms': 0.05, 'gap': 45, 'magType': 'md', 'type': 'earthquake', 'title': 'M 1.6 - 1 km ENE of The Geysers, CA'}, 'geometry': {'type': 'Point', 'coordinates': [-122.745330810547, 38.7826652526855, 0.25]}, 'id': 'nc75197676'}, {'type': 'Feature', 'properties': {'mag': 1.1, 'place': '11 km NW of Susitna, Alaska', 'time': 1750336029060, 'updated': 1750336137912, 'tz': None, 'url': 'https://earthquake.usgs.gov/earthquakes/eventpage/ak0257tco08q', 'detail': 'https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=ak0257tco08q&format=geojson', 'felt': None, 'cdi': None, 'mmi': None, 'alert': None, 'status': 'automatic', 'tsunami': 0, 'sig': 19, 'net': 'ak', 'code': '0257tco08q', 'ids': ',ak0257tco08q,', 'sources': ',ak,', 'types': ',origin,phase-data,', 'nst': None, 'dmin': None, 'rms': 0.37, 'gap': None, 'magType': 'ml', 'type': 'earthquake', 'title': 'M 1.1 - 11 km NW of Susitna, Alaska'}, 'geometry': {
        'type': 'Point', 'coordinates': [-150.6809, 61.6048, 71]}, 'id': 'ak0257tco08q'}, {'type': 'Feature', 'properties': {'mag': 2, 'place': '6 km SW of Alamo, CA', 'time': 1750335963250, 'updated': 1750338437013, 'tz': None, 'url': 'https://earthquake.usgs.gov/earthquakes/eventpage/nc75197671', 'detail': 'https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=nc75197671&format=geojson', 'felt': None, 'cdi': None, 'mmi': None, 'alert': None, 'status': 'automatic', 'tsunami': 0, 'sig': 62, 'net': 'nc', 'code': '75197671', 'ids': ',nc75197671,', 'sources': ',nc,', 'types': ',focal-mechanism,nearby-cities,origin,phase-data,scitech-link,', 'nst': 28, 'dmin': 0.008723, 'rms': 0.07, 'gap': 81, 'magType': 'md', 'type': 'earthquake', 'title': 'M 2.0 - 6 km SW of Alamo, CA'}, 'geometry': {'type': 'Point', 'coordinates': [-122.072830200195, 37.8125, 11.8500003814697]}, 'id': 'nc75197671'}, {'type': 'Feature', 'properties': {'mag': 0.92, 'place': '16 km W of Johannesburg, CA', 'time': 1750335889760, 'updated': 1750336093994, 'tz': None, 'url': 'https://earthquake.usgs.gov/earthquakes/eventpage/ci40998615', 'detail': 'https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=ci40998615&format=geojson', 'felt': None, 'cdi': None, 'mmi': None, 'alert': None, 'status': 'automatic', 'tsunami': 0, 'sig': 13, 'net': 'ci', 'code': '40998615', 'ids': ',ci40998615,', 'sources': ',ci,', 'types': ',nearby-cities,origin,phase-data,scitech-link,', 'nst': 33, 'dmin': 0.09568, 'rms': 0.16, 'gap': 65, 'magType': 'ml', 'type': 'earthquake', 'title': 'M 0.9 - 16 km W of Johannesburg, CA'}, 'geometry': {'type': 'Point', 'coordinates': [-117.8098333, 35.3586667, 6.39]}, 'id': 'ci40998615'}, {'type': 'Feature', 'properties': {'mag': 2.5, 'place': '1 km SE of Hilltop, Texas', 'time': 1750335778485, 'updated': 1750335917147, 'tz': None, 'url': 'https://earthquake.usgs.gov/earthquakes/eventpage/tx2025lzeizm', 'detail': 'https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=tx2025lzeizm&format=geojson', 'felt': None, 'cdi': None, 'mmi': None, 'alert': None, 'status': 'automatic', 'tsunami': 0, 'sig': 96, 'net': 'tx', 'code': '2025lzeizm', 'ids': ',tx2025lzeizm,', 'sources': ',tx,', 'types': ',origin,phase-data,', 'nst': 14, 'dmin': 0.4, 'rms': 0.4, 'gap': 207, 'magType': 'ml', 'type': 'earthquake', 'title': 'M 2.5 - 1 km SE of Hilltop, Texas'}, 'geometry': {'type': 'Point', 'coordinates': [-99.164, 28.683, 7.2186]}, 'id': 'tx2025lzeizm'}, {'type': 'Feature', 'properties': {'mag': 1.8, 'place': '7 km SE of Dilley, Texas', 'time': 1750335535826, 'updated': 1750335654096, 'tz': None, 'url': 'https://earthquake.usgs.gov/earthquakes/eventpage/tx2025lzefmw', 'detail': 'https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=tx2025lzefmw&format=geojson', 'felt': None, 'cdi': None, 'mmi': None, 'alert': None, 'status': 'automatic', 'tsunami': 0, 'sig': 50, 'net': 'tx', 'code': '2025lzefmw', 'ids': ',tx2025lzefmw,', 'sources': ',tx,', 'types': ',origin,phase-data,', 'nst': 10, 'dmin': 0.4, 'rms': 0.4, 'gap': 192, 'magType': 'ml', 'type': 'earthquake', 'title': 'M 1.8 - 7 km SE of Dilley, Texas'}, 'geometry': {'type': 'Point', 'coordinates': [-99.114, 28.621, 8.1962]}, 'id': 'tx2025lzefmw'}], 'bbox': [-150.6809, 28.621, 0.25, -99.114, 61.6048, 71]}


@fixture
def event_ids():
    return ["tx2025lmnxxe", "us6000qjtq",
            "2025lmnxxe", "0257ht85md",
            "tx2025lmnxxe", "us6000qjtq",
            "40992183", "40992167"]


@fixture
def event_urls():
    return ["https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/tx2025lmnxxe.geojson",
            "https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/us6000qjtq.geojson",
            "https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/2025lmnxxe.geojson",
            "https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/0257ht85md.geojson",
            "https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/tx2025lmnxxe.geojson",
            "https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/us6000qjtq.geojson",
            "https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/40992183.geojson",
            "https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/40992167.geojson"]

@fixture
def earthquake_data_with_unclean_events():
    return [{"properties": {"type": "earthquake",
                            "ids": "test_earthquake_id"}},
            {"properties": {"type": "earthquake",
                            "ids": "test_earthquake_id", "mag": "2.4"}},
            {"properties": {"type": "not an earthquake",
                            "ids": ["test_earthquake_id"],
                            "mag": "2.4"}},
            {"properties": {"type": "quarry",
                            "ids": ["test_earthquake_id"]}},
            {"prerties": {"type": "quarry",
                          "ids": ["test_earthquake_id"]}}
            ]


@fixture
def earthquake_data_with_unclean_events_cleaned():
    return [
        {"properties": {"type": "earthquake",
                        "ids": "test_earthquake_id"}},
        {"properties": {"type": "earthquake",
                        "ids": "test_earthquake_id", "mag": "2.4"}}]
