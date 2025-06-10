# Data Transitions

This document describes what the data should look like at every stage of the pipeline process.

## Extract

### INPUT

- Takes from USGS API.
- Endpoint: 

### OUTPUT

- Datatype: DataFrame.
- Example Data:
```python
pd.DataFrame({
    "type": "FeatureCollection",
    "metadata": {
        "generated": 1749484140000,
        "url": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson",
        "title": "USGS All Earthquakes, Past Hour",
        "status": 200,
        "api": "1.14.1",
        "count": 10
    },
    "features": [
        {
            "type": "Feature",
            "properties": {
                "mag": 1.6,
                "place": "20 km N of Mentone, Texas",
                "time": 1749483691255,
                "updated": 1749483896389,
                "tz": None,
                "url": "https://earthquake.usgs.gov/earthquakes/eventpage/tx2025lfsd",
                "detail": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/tx2025lfsd.geojson",
                "felt": None,
                "cdi": None,
                "mmi": None,
                "alert": None,
                "status": "automatic",
                "tsunami": 0,
                "sig": 39,
                "net": "tx",
                "code": "2025lfsd",
                "ids": ",tx2025lfsd,",
                "sources": ",tx,",
                "types": ",origin,phase-data,",
                "nst": 6,
                "dmin": 0.2,
                "rms": 0.7,
                "gap": 143,
                "magType": "ml",
                "type": "earthquake",
                "title": "M 1.6 - 20 km N of Mentone, Texas"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [-103.628, 31.891, 5]
            },
            "id": "tx2025lfsd"
        },
        {
            "type": "Feature",
            "properties": {
                "mag": 2.46,
                "place": "1 km E of Florence-Graham, CA",
                "time": 1749483214670,
                "updated": 1749483895060,
                "tz": None,
                "url": "https://earthquake.usgs.gov/earthquakes/eventpage/ci41180208",
                "detail": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/ci41180208.geojson",
                "felt": 13,
                "cdi": 3.4,
                "mmi": None,
                "alert": None,
                "status": "automatic",
                "tsunami": 0,
                "sig": 98,
                "net": "ci",
                "code": "41180208",
                "ids": ",ci41180208,",
                "sources": ",ci,",
                "types": ",dyfi,focal-mechanism,nearby-cities,origin,phase-data,scitech-link,",
                "nst": 123,
                "dmin": 0.02533,
                "rms": 0.26,
                "gap": 20,
                "magType": "ml",
                "type": "earthquake",
                "title": "M 2.5 - 1 km E of Florence-Graham, CA"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [-118.2351667, 33.9676667, 15.74]
            },
            "id": "ci41180208"
        },
        # ... (Remaining 8 features are similar in structure. You can repeat the pattern here.)
    ],
    "bbox": [-152.9611, 28.605, 0, -99.181, 65.3884, 16.2]
})
```

## Transform

### INPUT
- Datatype: DataFrame.
- DataFrame from Extract stage.
- See example data from above.

### OUTPUT
- Datatype: DataFrame.
- Refined DataFrame.
- Remove empty, null values.
- Example Data:
```python
pd.DataFrame({
    "id": ["tx2025lfsd", "ci41180208"],
    "magnitude": [1.6, 2.46],
    "time": [DateTime(<from 1749483214670>), DateTime(<from 1749483691255>)],
    "updated": [DateTime(<from 1749483214670>), DateTime(<from 1749483691255>)],
    "longitude": [-103.628, -118.2351667],
    "latitude": [31.891, 33.9676667],
    "depth": [5, 15.74],
    "url": ["iamcool.com", "scaryspooky.net"]
    "tsunami": [0, 0]
})
```

## Load

### INPUT
- Datatype: DataFrame.
- Refined DataFrame from Transform step.
- See example above.

### OUTPUT
- Upload data to RDS instance
