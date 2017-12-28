import json
import os
import urllib.request
from fuzzywuzzy import fuzz

datadir = '/Users/tgordon/projects/lexo/data/'

'''Wraps a list of dictionaries, each representing an exoplanet. The contents of the dictionary can be found in the 
documentation for the Exoplanet Archive at https://exoplanetarchive.ipac.caltech.edu/docs/program_interfaces.html'''
class PlanetTable:
    
    '''initializes a PlanetTable containing information from the Exoplanet Archive table given by tablename'''
    def __init__(self, tablename=''):
        self.tablename = tablename
        if self.__invalidtablename(self.tablename):
            raise ValueError('Invalid Tablename')
        filename = tablename + '.json'
        if self.__islocal(tablename):
            file = open(datadir + filename)
            self.table = json.load(file)
        else: 
            url = self.__buildurl(tablename)
            location = datadir + filename
            urllib.request.urlretrieve(url, location)
            self.table = json.load(open(location))
        if self.__islocal('names'):
            file = open(datadir + 'names.json')
            self.names_table = json.load(file)
        else:
            url = ('https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?' + 
            'table=cumulative&select=kepler_name,kepoi_name,kepid&format=json')
            location = datadir + 'names.json'
            urllib.request.urlretrieve(url, location)
            self.names_table = json.load(open(location))
    
    '''Returns True if the tablename is one of the tables from the Exoplanet Archive, False otherwise.'''
    def __invalidtablename(self, tablename):
        validtablenames = 'exoplanets', 'multiexopars', 'aliastable', 'cumulative', ''
        return not (tablename in validtablenames)
    
    '''Returns True if the data for tablename is in the local directory, False otherwise'''
    def __islocal(self, tablename):
        filename = tablename + '.json'
        return filename in os.listdir(datadir)
    
    '''Builds a query string to query for the parameters listed in filename.'''
    def __buildstring(self, filename):
        f = open(filename)
        string = ''
        for line in f:
            line = line[:-1]
            string = string + line + ','
        return string[:-1]
    
    '''Builds the URL to query for the parameters listed in filename in the table tablename'''
    def __buildurl(self, tablename):
        baseurl = 'https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table='
        # confirmed planets
        if tablename == 'exoplanets':
            urlend = 'exoplanets&select=' + self.__buildstring(datadir + 'pl_columns.txt') + '&format=json'
        # extended confirmed planet info
        if tablename == 'multiexopars':
            urlend = 'multiexopars&select=' + self.__buildstring(datadir + 'mpl_columns.txt') + '&format=json'
        # other names for star
        if tablename == 'aliastable':
            urlend = 'aliastable@objname='
        # koi table
        if tablename == 'cumulative':
            urlend = 'cumulative&select=' + self.__buildstring(datadir + 'koi_columns.txt') + '&format=json'
        # time series 
        if tablename == 'keplertimeseries':
            urlend = 'keplertimeseries&kepid='
        return baseurl + urlend
    
    '''Returns True if the value is within lims.'''
    def __inrange(self, value, lims):
        if value is None:
            return False
        return value <= lims[1] and value >= lims[0]
    
    '''Returns a list of dictionaries for which parameter is within lims.'''
    def findinrange(self, parameter, lims):
        ret = []
        for d in self.table:
            if self.__inrange(d[parameter], lims):
                ret.append(d)
        return ret
    
    '''Returns a list of dictionaries for which the parameter has the given value.'''
    def find(self, parameter, value):
        ret = []
        for d in self.table:
            if d[parameter] == value:
                ret.append(d)
        return ret
    
    '''Returns the dictionary '''
    def fuzzymatch(self, name):
        ratios = []
        for d in self.table:
            ratios.append(fuzz.token_sort_ratio(name, d['pl_name']))
        return self.table[ratios.index(max(ratios))], max(ratios)
