# Pipeline

## Extract

- Reads from https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson .

- This updates every minute but stores an hours worth of data.

    - How to avoid repeated data?


### Thought Process

- Tried to use ObsPy and ObsPlus to get data from the API and convert it to a dataframe.

- ObsPlus wanted a version on python with `tkinter`. I could do this now but it seems like it could cause more issues down the line.

- I can still use ObsPy to get the data (I've considered the alternative of removing this library and calling the API directly, however it seems using obspy will make it easier to expand the project to different data sources in the future).

- Now the big question is how to get the `ObsPy.Catalog` object into a `pd.DataFrame`.

    - Option one: convert to JSON then use a Panda's built-in.

    - Option two: convert directly to a DataFrame.

- If I'm not getting the data in as a JSON, it makes more sense to go straight to a df. However there is write support for JSON in ObsPy.

    - What is in an ObsPy JSON? Is it just going to be the QuakeML or will it be formatted properly?

- I'm going to try the following route:  
    - `obspy.clients.fdsn.client.Client.get_events()` --`obspy.Catalog`-->
    - `obspy.io.json()` --`JSON`-->
    - `pd.read_json()` --`pd.DataFrame`--> `transform.py`.




Is this missing any data we need?

- magnitude there
- time there
- updated there
- latitude/longitude/depth(?) in geometry.coordinates
- url there
- tsunami there

- Convert into dataframe.
- No need to obspy?
