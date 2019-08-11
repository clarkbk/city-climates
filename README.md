Given a set of U.S. cities (i.e. weather stations) and climate measures, scrapes monthly 1981-2010 climate normals from the NOAA's National Centers for Environmental Information (NCEI).

## Installation

```bash
$ mkvirtualenv city-climates
# (clone this repo)
$ cd city-climates
$ pip install -r requirements.txt
```

## Configuration

Choose your cities and find station IDs on https://www.ncdc.noaa.gov.

Choose statistics from https://www1.ncdc.noaa.gov/pub/data/normals/1981-2010/readme.txt. Include the normalization factor for each statistic. (For example, if the statistic is provided in units of tenths of degrees, then the factor should be `0.1`.)

Edit and save `objects.py`.

## Use

```bash
$ python3 run.py
```

A file named `output.csv` containing a summary of the requested statistics will be saved into the main project directory.
