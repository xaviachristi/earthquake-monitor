# ObsPy Introduction

## What is ObsPy?

- ObsPy is a python framework for working with seismological data.


## What is its role in this project?

- The part of ObsPy we are concerned with is its [handling of events](https://docs.obspy.org/packages/index.html#:~:text=Event%20Data%20Import/Export%20Plug%2Dins) (as compared to its main focus, which is on the readings from seismometers).
- [`obspy.core.event.read_events()`](https://docs.obspy.org/packages/autogen/obspy.core.event.read_events.html#obspy-core-event-read-events) supports QuakeML natively.
- It returns an ObsPy `Catalog` object.
- The [ObsPlus](https://niosh-mining.github.io/obsplus/versions/latest/index.html) library provides ObsPy support for Pandas dataframes.
- ObsPlus has an `obsplus.picks_to_df()` function which can construct summary dataframes from objects including the obspy `catalog`.

## Example snippets (taken from documentation)

Example for `read_events()`
```
import obspy
cat = obspy.read_events("/path/to/file") # Also accepts URLs.
```

Example for `picks_to_df()`
```
import obsplus
crandall = obsplus.load_dataset("crandall_test")
cat = crandall.event_client.get_events()
ev_df = obsplus.events_to_df(cat)
```
Produces a DataFrame that includes these headings:
```
- time
- latitude
- longitude
- depth
- magnitude
- event_description
- associated_phase_count
- azimuthal_gap
- event_id
- horizontal_uncertainty
- standard_error
- used_phase_count
- ...


## Additional Notes

- Reading seismograms is not currently in scope.
- Should this become necessary:
    - `obspy.io.json` is for writing JSON (no mention of reading).
    - `obspy.io.quakeml` is for reading and writing QuakeML specifically.
