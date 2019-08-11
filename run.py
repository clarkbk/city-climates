import csv
import requests

from objects import City, Statistic, DataRow

base_url = 'https://www1.ncdc.noaa.gov/pub/data/normals/1981-2010/products/station/'

with open('output.csv', 'w') as f:
    writer = csv.writer(f)
    headers = [
        'Statistic',
        'Jan',
        'Feb',
        'Mar',
        'Apr',
        'May',
        'Jun',
        'Jul',
        'Aug',
        'Sep',
        'Oct',
        'Nov',
        'Dec',
    ]

    for city in City.get_instances():
        url = base_url + f'{city.station_id}.normals.txt'
        r = requests.get(url)

        print(city.name, file=f)
        writer.writerow(headers)

        for line in r.iter_lines():
            split_at = 23
            stat_name = line[:split_at].strip().decode('UTF-8')

            if stat_name not in Statistic.get_names():
                continue

            stat = Statistic.get_instance_by_name(stat_name)

            raw_data = line[split_at:]
            d = DataRow(stat, raw_data)
            writer.writerow(d.process())

        print('\n', file=f)
