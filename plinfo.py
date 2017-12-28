from PlanetTable import PlanetTable
from Body import Planet, Star
import sys

dt = PlanetTable('exoplanets')
#def find_planet(dt, name):
#    for d in dt: 
#        if (d['pl_hostname'] + ' ' + d['pl_letter']) == name:
#            return Planet(d)
#    return None

planet, match = dt.fuzzymatch(sys.argv[1])
planet = Planet(planet)
if match < 99:
    print()
    print("No exact match. Showing closest match.")
#planet = find_planet(dt.table, sys.argv[1])
if planet is None: 
    print("planet not found in table")
else:
    print('\n---------------PLANET---------------')
    print(planet)
    print('\n----------------STAR----------------')
    print(planet.star)
    print('\n----------UPCOMING TRANSITS---------')
    transits = planet.get_transits_string(365)
    if len(transits) > 0:
        print('\n         earliest               likeliest                latest')
        for i, times in enumerate(transits):
            if i < 10:
                 print(times)
            if i == 11: 
                 print('+ ' + str(len(transits)-11) + ' more transits in the next year')
        print('\n')
    else:
        print()
        print("No transit data")
        print()
