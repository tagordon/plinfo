import numpy as np
from uncertainties import ufloat
from astropy.time import Time
import astropy.constants as ac

'''For a given key from the dictionary, sets a ufloat variable which contains the maximum likelihood value and 1-sigma error bars.'''
def setvalue(planet_dict, key):
    if key[0:3] == 'kep':
        err1key = key + '_err1'
        err2key = key + '_err2'
    else: 
        err1key = key + 'err1'
        err2key = key + 'err2'
    if planet_dict[key] is None:
        return None
    try: 
        value = ufloat(planet_dict[key], max(abs(planet_dict[err1key]), abs(planet_dict[err2key])))
    except:
        value = ufloat(planet_dict[key], 0)
    return value

'''A Star object represents the parent body of an exoplanet, containing its name, radius, mass, effective temperature, age, luminsity, metallicity, the number of planets known to orbit it, its distance from the earth, and u, b, and v magnitudes if available.'''
class Star:
    
    def __init__(self, planet_dict):
        self.planet_dict = planet_dict
        prefix = list(planet_dict.keys())[0][0:3]
        if prefix == 'pl_' or prefix == 'st_':
            self.name = planet_dict['pl_hostname']
            self.radius = setvalue(planet_dict, 'st_rad')
            self.mass = setvalue(planet_dict, 'st_mass')
            self.teff = setvalue(planet_dict, 'st_teff')
            self.age = setvalue(planet_dict, 'st_age')
            self.luminosity = setvalue(planet_dict, 'st_lum')
            self.metallicity = setvalue(planet_dict, 'st_metfe')
            self.n_planets = planet_dict['pl_pnum']
            self.distance = planet_dict['st_dist']
            try:
                self.umag = ufloat(planet_dict['st_uj'], planet_dict['st_ujerr'])
            except: 
                self.umag = None
            try:
                self.bmag = ufloat(planet_dict['st_bj'], planet_dict['st_bjerr']) 
            except: 
                self.bmag = None
            try: 
                self.vmag = ufloat(planet_dict['st_vj'], planet_dict['st_vjerr'])
            except:
                self.vmag = None
        if prefix == 'mpl' or prefix == 'mst':
            self.name = planet_dict['mpl_hostname']
            self.radius = setvalue(planet_dict, 'mst_rad')
            self.mass = setvalue(planet_dict, 'mst_mass')
            self.teff = setvalue(planet_dict, 'mst_teff')
            self.age = setvalue(planet_dict, 'mst_age')
            self.luminosity = setvalue(planet_dict, 'mst_lum')
            self.metallicity = setvalue(planet_dict, 'mst_metfe')
            self.n_planets = planet_dict['mpl_pnum']
            self.distance = None
            self.umag = None
            self.bmag = None
            self.vmag = None
        if prefix == 'kep' or prefix == 'koi':
            self.name = planet_dict['kepoi_name']
            self.radius = setvalue(planet_dict, 'koi_srad')
            self.mass = setvalue(planet_dict, 'koi_smass')
            self.teff = setvalue(planet_dict, 'koi_steff')
            self.age = setvalue(planet_dict, 'koi_sage')
            self.luminosity = None
            self.metallicity = setvalue(planet_dict, 'koi_smet')
            self.n_planets = setvalue(planet_dict, 'koi_count')
            self.distance = None
            self.umag = None
            self.bmag = None
            self.vmag = None
            
    '''A string representation of the star.'''        
    def __str__(self):
        pad = 27
        return ("\nname: ".ljust(pad) + self.name + 
                "\nmass (solar): ".ljust(pad) + str(self.mass) + 
                "\neffective temp: ".ljust(pad) + str(self.teff) + 
                "\nmetallicity: ".ljust(pad) + str(self.metallicity) + 
                "\nluminosity (solar): ".ljust(pad) + str(self.luminosity) + 
                "\nradius (solar): ".ljust(pad) + str(self.radius) + 
                "\nage (Byr): ".ljust(pad) + str(self.age) + 
                "\ndistance (pc)".ljust(pad) + str(self.distance) +
                "\nJohnson v-band mag: ".ljust(pad) + str(self.vmag) + 
                "\nnumber of planets: ".ljust(pad) + str(self.n_planets))
    
'''A Planet object represents an exoplanet, containing its name, radius, mass, period, semimajor axis, eccentricity, transit duration, midpoint, and depth, and a flag noting whether or not its transits exhibit ttvs.'''
class Planet:
    
    def __init__(self, planet_dict):
        prefix = list(planet_dict.keys())[0][0:3]
        self.planet_dict = planet_dict
        if prefix == 'pl_' or prefix == 'st_':
            self.name = planet_dict['pl_hostname'] + ' ' + planet_dict['pl_letter']
            self.radius = setvalue(planet_dict, 'pl_radj')
            self.mass = setvalue(planet_dict, 'pl_bmassj')
            self.period = setvalue(planet_dict, 'pl_orbper')
            self.semimajor_axis = setvalue(planet_dict, 'pl_orbsmax')
            self.eccentricity = setvalue(planet_dict, 'pl_orbeccen')
            self.transit_mid = setvalue(planet_dict, 'pl_tranmid')
            self.transit_dur = setvalue(planet_dict, 'pl_trandur')
            self.transit_depth = setvalue(planet_dict, 'pl_trandep')
            if self.transit_depth is not None:
                self.transit_depth *= 1e4 # ppm 
            self.ttvs = planet_dict['pl_ttvflag']
        if prefix == 'mpl' or prefix == 'mst_':
            self.name = planet_dict['mpl_hostname']
            self.radius = setvalue(planet_dict, 'mpl_radj')
            self.mass = setvalue(planet_dict, 'mpl_bmassj')
            self.period = setvalue(planet_dict, 'mpl_orbper')
            self.semimajor_axis = setvalue(planet_dict, 'mpl_orbsmax')
            self.eccentricity = setvalue(planet_dict, 'mpl_orbeccen')
            self.transit_mid = setvalue(planet_dict, 'mpl_tranmid')
            self.transit_dur = setvalue(planet_dict, 'mpl_trandur')
            self.transit_depth = setvalue(planet_dict, 'mpl_trandep')
            if self.transit_depth is not None:
                self.transit_depth *= 1e4 # ppm 
            self.ttvs = planet_dict['mpl_ttvflag']
        if prefix == 'kep' or prefix == 'koi':
            self.name = planet_dict['kepoi_name']
            self.radius = setvalue(planet_dict, 'koi_prad')
            if self.radius is not None:
                self.radius *= (ac.R_earth.value/ac.R_jup.value)
            self.mass = None
            self.period = setvalue(planet_dict, 'koi_period')
            self.semimajor_axis = setvalue(planet_dict, 'koi_sma')
            self.eccentricity = setvalue(planet_dict, 'koi_eccen')
            self.transit_mid = setvalue(planet_dict, 'koi_time0')
            self.transit_dur = setvalue(planet_dict, 'koi_duration')
            self.transit_depth = setvalue(planet_dict, 'koi_depth') # already in ppm
            self.ttvs = None
            
        self.star = Star(self.planet_dict)
        
    '''A string representation of a planet'''    
    def __str__(self):
        pad = 27
        if self.ttvs: 
            ttvflag = 'yes'
        else: 
            ttvflag = 'no'
        return ("\nname: ".ljust(pad) + self.name + 
                "\nradius (jupiter): ".ljust(pad) + str(self.radius) + 
                "\nsemimajor axis (au): ".ljust(pad) + str(self.semimajor_axis) + 
                "\nperiod (days): ".ljust(pad) + str(self.period) + 
                "\ntransit depth: ".ljust(pad) + str(self.transit_depth) + 
                "\nmass (jupiter): ".ljust(pad) + str(self.mass) + 
                "\neccentricity: ".ljust(pad) + str(self.eccentricity) + 
                "\ntransit duration (days): ".ljust(pad) + str(self.transit_dur) + 
                "\nttvs? ".ljust(pad) + ttvflag)
    
    '''Returns the start time of the transit in julian days.'''
    def __t0(self):
        if (self.transit_mid is not None) and (self.transit_dur is not None):
            return self.transit_mid - 0.5*self.transit_dur
        else: 
            return None
    
    '''Returns the n-th transit time after the first recorded transit of the planet.'''
    def __transit_times(self, n):
        return self.__t0() + n*self.period
    
    '''Returns all the transits between start and start + dt (in julian days).'''
    def get_transits(self, dt, start):
        start += Time.now().jd
        if self.__t0() is not None:
            first_transit = np.floor((start - self.__t0().nominal_value)/self.period.nominal_value) + 1
            n_transits = np.floor(dt/self.period.nominal_value)
            n = np.arange(first_transit, first_transit+n_transits)
            return [self.__transit_times(n) for n in n]
        else:
            return None
    
    '''Returns a string representation of all the transits between start and start + dt.'''
    def get_transits_string(self, dt, start=0):
        transits = self.get_transits(dt, start)
        if transits is not None:
            transit_nom = [Time(t.nominal_value, format='jd').iso for t in transits]
            transit_minus = [Time(t.nominal_value - t.std_dev, format='jd').iso for t in transits]
            transit_plus = [Time(t.nominal_value + t.std_dev, format='jd').iso for t in transits]
            ret = []
            for i in range(len(transit_nom)):
                ret.append(transit_minus[i] + ' | ' + transit_nom[i] + ' | ' + transit_plus[i])
            return ret
        else: 
            return []
