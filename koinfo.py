from DataTable import DataTable
from Object import Planet, Star
import sys

dt = DataTable('cumulative')
def find_planet(dt, name):
    for d in dt: 
        if d['kepoi_name'] == name:
            return Planet(d)
    return None

planet = find_planet(dt.table, sys.argv[1])
if planet is None: 
    print("planet not found in table")
else:
    print('\n---------------PLANET---------------')
    print(planet)
    print('\n----------------STAR----------------')
    print(planet.star)
    print('\n----------UPCOMING TRANSITS---------')
    print('\n         earliest               likeliest                latest')
    transits = planet.get_transits_string(365)
    if transits is not None:
        for i, times in enumerate(transits):
            if i < 10:
                 print(times)
            if i == 11: 
                 print('+ ' + str(len(transits)-11) + ' more transits in the next year')
        print('\n')
    else:
        print(None)
