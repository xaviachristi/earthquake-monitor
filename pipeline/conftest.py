"""Fixtures for tests in this directory."""
from json import loads
from unittest.mock import MagicMock

from pytest import fixture
from pandas import DataFrame
from obspy.core.event.catalog import _create_example_catalog


@fixture
def example_catalog():
    """An example catalog for use with the ObsPy library."""
    return _create_example_catalog()


@fixture
def example_detailed_event():
    """An example of a detailed USGS API response."""
    return loads("""{"type": "Feature","properties":{"mag":0.53,"place":"10 km SSW of Idyllwild, CA","time":1749655031680,"updated":1749675581157,"tz":null,"url":"https://earthquake.usgs.gov/earthquakes/eventpage/ci41182664","felt":null,"cdi":null,"mmi":null,"alert":null,"status":"reviewed","tsunami":0,"sig":4,"net":"ci","code":"41182664","ids":",ci41182664,","sources":",ci,","types":",nearby-cities,origin,phase-data,scitech-link,","nst":15,"dmin":0.06854,"rms":0.13,"gap":115,"magType":"ml","type":"earthquake","title":"M 0.5 - 10 km SSW of Idyllwild, CA","products":{"nearby-cities":[{"indexid":5431596,"indexTime":1749675579811,"id":"urn:usgs-product:ci:nearby-cities:ci41182664:1749675578440","type":"nearby-cities","code":"ci41182664","source":"ci","updateTime":1749675578440,"status":"UPDATE","properties":{"eventsource":"ci","eventsourcecode":"41182664","pdl-client-version":"Version 2.7.10 2021-06-21"},"preferredWeight":7,"contents":{"nearby-cities.json":{"contentType":"application/json","lastModified":1749675578000,"length":596,"url":"https://earthquake.usgs.gov/realtime/product/nearby-cities/ci41182664/ci/1749675578440/nearby-cities.json"}}}],"origin":[{"indexid":5431595,"indexTime":1749675578850,"id":"urn:usgs-product:ci:origin:ci41182664:1749675577830","type":"origin","code":"ci41182664","source":"ci","updateTime":1749675577830,"status":"UPDATE","properties":{"azimuthal-gap":"115","depth":"15.81","depth-type":"from location","error-ellipse-azimuth":"357","error-ellipse-intermediate":"768","error-ellipse-major":"1248","error-ellipse-minor":"552","error-ellipse-plunge":"75","error-ellipse-rotation":"10","evaluation-status":"final","event-type":"earthquake","eventParametersPublicID":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?eventid=41182664","eventsource":"ci","eventsourcecode":"41182664","eventtime":"2025-06-11T15:17:11.680Z","horizontal-error":"0.31","latitude":"33.6663333","longitude":"-116.771","magnitude":"0.53","magnitude-azimuthal-gap":"123.5","magnitude-error":"0.206","magnitude-num-stations-used":"7","magnitude-source":"CI","magnitude-type":"ml","minimum-distance":"0.06854","num-phases-used":"28","num-stations-used":"15","origin-source":"CI","pdl-client-version":"Version 2.7.10 2021-06-21","quakeml-magnitude-publicid":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?magnitudeid=109412373","quakeml-origin-publicid":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?originid=105898557","quakeml-publicid":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?eventid=41182664","review-status":"reviewed","standard-error":"0.13","title":"10 km SSW of Idyllwild, CA","version":"6","vertical-error":"0.51"},"preferredWeight":157,"contents":{"contents.xml":{"contentType":"application/xml","lastModified":1749675578000,"length":195,"url":"https://earthquake.usgs.gov/realtime/product/origin/ci41182664/ci/1749675577830/contents.xml"},"quakeml.xml":{"contentType":"application/xml","lastModified":1749675577000,"length":3423,"url":"https://earthquake.usgs.gov/realtime/product/origin/ci41182664/ci/1749675577830/quakeml.xml"}}}],"phase-data":[{"indexid":5431597,"indexTime":1749675580880,"id":"urn:usgs-product:ci:phase-data:ci41182664:1749675577830","type":"phase-data","code":"ci41182664","source":"ci","updateTime":1749675577830,"status":"UPDATE","properties":{"azimuthal-gap":"115","depth":"15.81","depth-type":"from location","error-ellipse-azimuth":"357","error-ellipse-intermediate":"768","error-ellipse-major":"1248","error-ellipse-minor":"552","error-ellipse-plunge":"75","error-ellipse-rotation":"10","evaluation-status":"final","event-type":"earthquake","eventParametersPublicID":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?eventid=41182664","eventsource":"ci","eventsourcecode":"41182664","eventtime":"2025-06-11T15:17:11.680Z","horizontal-error":"0.31","latitude":"33.6663333","longitude":"-116.771","magnitude":"0.53","magnitude-azimuthal-gap":"123.5","magnitude-error":"0.206","magnitude-num-stations-used":"7","magnitude-source":"CI","magnitude-type":"ml","minimum-distance":"0.06854","num-phases-used":"28","num-stations-used":"15","origin-source":"CI","pdl-client-version":"Version 2.7.10 2021-06-21","quakeml-magnitude-publicid":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?magnitudeid=109412373","quakeml-origin-publicid":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?originid=105898557","quakeml-publicid":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?eventid=41182664","review-status":"reviewed","standard-error":"0.13","title":"10 km SSW of Idyllwild, CA","version":"6","vertical-error":"0.51"},"preferredWeight":157,"contents":{"contents.xml":{"contentType":"application/xml","lastModified":1749675578000,"length":195,"url":"https://earthquake.usgs.gov/realtime/product/phase-data/ci41182664/ci/1749675577830/contents.xml"},"quakeml.xml":{"contentType":"application/xml","lastModified":1749675577000,"length":100216,"url":"https://earthquake.usgs.gov/realtime/product/phase-data/ci41182664/ci/1749675577830/quakeml.xml"}}}],"scitech-link":[{"indexid":5431598,"indexTime":1749675582101,"id":"urn:usgs-product:ci:scitech-link:ci41182664-waveform_ci:1749675581157","type":"scitech-link","code":"ci41182664-waveform_ci","source":"ci","updateTime":1749675581157,"status":"UPDATE","properties":{"addon-code":"Waveform_CI","addon-type":"LinkURL","eventsource":"ci","eventsourcecode":"41182664","pdl-client-version":"Version 2.7.10 2021-06-21","text":"Waveforms","url":"https://scedc.caltech.edu/review_eventfiles/makePublicView.html?evid=41182664","version":"01"},"preferredWeight":7,"contents":[]}]}},"geometry":{"type":"Point","coordinates":[-116.771,33.6663333,15.81]},"id":"ci41182664"}""")


@fixture
def expected_columns():
    """List of columns expected from sql query to database."""
    return [
        "earthquake_id", "magnitude", "time", "updated", "longitude", "latitude",
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
            "time": "2024-01-01", "updated": "2024-01-02", "depth": 5.0, "url": "example.com",
            "felt": 1, "tsunami": 0, "cdi": 3.1, "mmi": 2.3, "nst": 1,
            "sig": 1, "net": "us", "dmin": 0.1, "alert": "green",
            "location_source": "us", "magnitude_type": "mb",
            "state_name": "California", "region_name": "West Coast",
            "state_id": 12, "region_id": 4
        },
        {
            "earthquake_id": 2, "magnitude": 4.0, "latitude": 11.0, "longitude": 21.0,
            "time": "2024-02-01", "updated": "2024-02-02", "depth": 10.0, "url": "another.com",
            "felt": 2, "tsunami": 1, "cdi": 3.0, "mmi": 2.5, "nst": 5,
            "sig": 100, "net": "us", "dmin": 0.1, "alert": "green",
            "location_source": "us", "magnitude_type": "mb",
            "state_name": "Nevada", "region_name": "West Coast",
            "state_id": 13, "region_id": 4
        }
    ])


@fixture
def example_df2():
    """Second example dataframe with one duplicate entry from example_df."""
    return DataFrame([
        {
            "earthquake_id": 1, "magnitude": 2.5, "latitude": 10.0, "longitude": 20.0,
            "time": "2024-01-01", "updated": "2024-01-02", "depth": 5.0, "url": "example.com",
            "felt": 1, "tsunami": 0, "cdi": 3.1, "mmi": 2.3, "nst": 1,
            "sig": 1, "net": "us", "dmin": 0.1, "alert": "green",
            "location_source": "us", "magnitude_type": "mb",
            "state_name": "California", "region_name": "West Coast"
        }
    ])


@fixture
def example_diff():
    """Expected difference between example_df and example_df2 (only the unique row)."""
    return DataFrame([
        {
            "magnitude": 4.0, "latitude": 11.0, "longitude": 21.0,
            "time": "2024-02-01", "updated": "2024-02-02", "depth": 10.0, "url": "another.com",
            "felt": 2, "tsunami": 1, "cdi": 3.0, "mmi": 2.5, "nst": 5,
            "sig": 100, "net": "us", "dmin": 0.1, "alert": "green",
            "location_source": "us", "magnitude_type": "mb",
            "state_name": "Nevada", "region_name": "West Coast"
        }
    ])
