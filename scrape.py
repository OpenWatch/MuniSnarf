#!/usr/bin/env python

from peewee import *
from model import Muni, Location
from googleplaces import GooglePlaces, types, lang

import datetime
import urllib2
import json
import pprint

from local_settings import GOOGLE_KEYS

#Settings
DATABASE = 'muni.db'
database = SqliteDatabase(DATABASE)
TORCTL_PASS="derp"
code_to_state = {"WA": "WASHINGTON", "VA": "VIRGINIA", "DE": "DELAWARE", "DC": "DISTRICT OF COLUMBIA", "WI": "WISCONSIN", "WV": "WEST VIRGINIA", "HI": "HAWAII", "AE": "Armed Forces Middle East", "FL": "FLORIDA", "FM": "FEDERATED STATES OF MICRONESIA", "WY": "WYOMING", "NH": "NEW HAMPSHIRE", "NJ": "NEW JERSEY", "NM": "NEW MEXICO", "TX": "TEXAS", "LA": "LOUISIANA", "NC": "NORTH CAROLINA", "ND": "NORTH DAKOTA", "NE": "NEBRASKA", "TN": "TENNESSEE", "NY": "NEW YORK", "PA": "PENNSYLVANIA", "CA": "CALIFORNIA", "NV": "NEVADA", "AA": "Armed Forces Americas", "PW": "PALAU", "GU": "GUAM", "CO": "COLORADO", "VI": "VIRGIN ISLANDS", "AK": "ALASKA", "AL": "ALABAMA", "AP": "Armed Forces Pacific", "AS": "AMERICAN SAMOA", "AR": "ARKANSAS", "VT": "VERMONT", "IL": "ILLINOIS", "GA": "GEORGIA", "IN": "INDIANA", "IA": "IOWA", "OK": "OKLAHOMA", "AZ": "ARIZONA", "ID": "IDAHO", "CT": "CONNECTICUT", "ME": "MAINE", "MD": "MARYLAND", "MA": "MASSACHUSETTS", "OH": "OHIO", "UT": "UTAH", "MO": "MISSOURI", "MN": "MINNESOTA", "MI": "MICHIGAN", "MH": "MARSHALL ISLANDS", "RI": "RHODE ISLAND", "KS": "KANSAS", "MT": "MONTANA", "MP": "NORTHERN MARIANA ISLANDS", "MS": "MISSISSIPPI", "PR": "PUERTO RICO", "SC": "SOUTH CAROLINA", "KY": "KENTUCKY", "OR": "OREGON", "SD": "SOUTH DAKOTA"}

# Org types to scrape
ORG_TYPES = ['police', 'fire', 'city hall', 'newspaper', 'tv station', 'hospital']

# Are we going through Tor?
def check_tor():
    conn = TorCtl.connect(passphrase=TORCTL_PASS)
    if conn:
        return True
    else:
        return False
# Tell Tor we want a new Exit Node
# Make sure Tor has a control channel open!
def get_new_address():
    conn = TorCtl.connect(passphrase=TORCTL_PASS)
    conn.sendAndRecv('signal newnym\r\n')
    conn.close()
    time.sleep(10)

def p_print(data):
    pprint.pprint(data)

def setup_db():
    database.connect()
    try:
        Muni.create_table() #only needed once
    except Exception, e:
        return

def zipit():

    ifile  = open('zipcodes.csv', "rb")
    reader = csv.reader(ifile)

    rownum = 0
    for row in reader:
        #"Zipcode","ZipCodeType","City","State","LocationType","Lat","Long","Location","Decommisioned","TaxReturnsFiled","EstimatedPopulation","TotalWages"
        
        # Fuck the header row.
        if rownum == 0:
            rownum+=1
            continue

        l = Location()
        l.zip_code = row[0]
        l.city = slugify(row[2])
        l.state_code = row[3]
        l.state = slugify(code_to_state[row[3]])
        l.lat = row[5]
        l.lon = row[6]

        if l.lat is not "":
            l.save()

        rownum += 1

    ifile.close()

def scrape():
    return


def item_in_db(zip_code, org):
    try:
        Muni.get(Muni.zip_code == id, Muni.org == org)
        return True
    except Exception, e:
        return False

def add_item(result):
    if result['target']:
        target = result['target']['url']
    else:
        target = "No target"

    e = Muni.create(    
                zip = result['zip_code']
                )
    return e

def get_all_events():
    for m in Muni.select():
        print m

setup_db()
scrape()
get_all_events()
