import weakref

from textwrap import wrap
from collections import defaultdict


class Base(object):
    __refs__ = defaultdict(list)

    def __init__(self):
        self.__refs__[self.__class__].append(weakref.ref(self))

    @classmethod
    def get_instances(cls):
        for inst_ref in cls.__refs__[cls]:
            inst = inst_ref()
            if inst is not None:
                yield inst

    @classmethod
    def get_names(cls):
        return [ref().name for ref in cls.__refs__[cls]]

    @classmethod
    def get_instance_by_name(cls, name):
        for inst_ref in cls.__refs__[cls]:
            inst = inst_ref()
            if inst.name == name:
                return inst


class City(Base):
    def __init__(self, slug, station_id):
        super(City, self).__init__()

        self.slug = slug
        self.station_id = station_id

    @property
    def name(self):
        return self.slug.replace('_', ' ').title()


class Statistic(Base):
    def __init__(self, name, factor):
        super(Statistic, self).__init__()

        self.name = name
        self.factor = factor


class DataRow(object):
    def __init__(self, statistic, raw_line):
        self.statistic = statistic
        self.raw_values = [x.strip() for x in wrap(raw_line.decode('UTF-8'), 7)]

    def process(self):
        values = [self.statistic.name]
        for value in self.raw_values:
            value = int(value[:-1])

            if value == -7777:
                value = 0

            values.append(value * self.statistic.factor)

        try:
            assert len(values) == 13
        except AssertionError as e:
            print('Incorrect number of values in row ({len(values)})')
            raise e

        return values


city_stations = {
    'atlanta':          'USW00013874',
    'austin':           'USW00013904',
    'boise':            'USW00024131',
    'chicago':          'USW00094846',
    'denver':           'USW00003017',
    'minneapolis':      'USW00014922',
    'nashville':        'USW00013897',
    'new_york_city':    'USW00094789',
    'phoenix':          'USW00023183',
    'salt_lake_city':   'USW00024127',
    'san_diego':        'USW00023188',
    'san_francisco':    'USW00023272',
    'seattle':          'USW00024233',
}

stat_factors = {
    # temperature
    'mly-tmax-normal':          0.1,
    'mly-tavg-normal':          0.1,
    'mly-tmin-normal':          0.1,
    'mly-tmax-avgnds-grth090':  0.1,
    'mly-tmin-avgnds-lsth040':  0.1,
    # precipitation
    'mly-prcp-normal':          0.01,
    'mly-snow-normal':          0.1,
    'mly-prcp-avgnds-ge050hi':  0.1,
    'mly-snow-avgnds-ge050ti':  0.1,
    'mly-snwd-avgnds-ge001wi':  0.1,
}


cities = []
for cs in city_stations.items():
    c = City(*cs)
    cities.append(c)

statistics = []
for sf in stat_factors.items():
    s = Statistic(*sf)
    statistics.append(s)
