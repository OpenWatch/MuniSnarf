#!/usr/bin/env python

from peewee import *
from model import Muni, Location
from googleplaces import GooglePlaces, types, lang

import datetime
import urllib2
import json
import pprint
import random
import csv
import time
from django.template.defaultfilters import slugify

from local_settings import GOOGLE_KEYS

#Settings
DATABASE = 'muni.db'
database = SqliteDatabase(DATABASE)
TORCTL_PASS="derp"
code_to_state = {"WA": "WASHINGTON", "VA": "VIRGINIA", "DE": "DELAWARE", "DC": "DISTRICT OF COLUMBIA", "WI": "WISCONSIN", "WV": "WEST VIRGINIA", "HI": "HAWAII", "AE": "Armed Forces Middle East", "FL": "FLORIDA", "FM": "FEDERATED STATES OF MICRONESIA", "WY": "WYOMING", "NH": "NEW HAMPSHIRE", "NJ": "NEW JERSEY", "NM": "NEW MEXICO", "TX": "TEXAS", "LA": "LOUISIANA", "NC": "NORTH CAROLINA", "ND": "NORTH DAKOTA", "NE": "NEBRASKA", "TN": "TENNESSEE", "NY": "NEW YORK", "PA": "PENNSYLVANIA", "CA": "CALIFORNIA", "NV": "NEVADA", "AA": "Armed Forces Americas", "PW": "PALAU", "GU": "GUAM", "CO": "COLORADO", "VI": "VIRGIN ISLANDS", "AK": "ALASKA", "AL": "ALABAMA", "AP": "Armed Forces Pacific", "AS": "AMERICAN SAMOA", "AR": "ARKANSAS", "VT": "VERMONT", "IL": "ILLINOIS", "GA": "GEORGIA", "IN": "INDIANA", "IA": "IOWA", "OK": "OKLAHOMA", "AZ": "ARIZONA", "ID": "IDAHO", "CT": "CONNECTICUT", "ME": "MAINE", "MD": "MARYLAND", "MA": "MASSACHUSETTS", "OH": "OHIO", "UT": "UTAH", "MO": "MISSOURI", "MN": "MINNESOTA", "MI": "MICHIGAN", "MH": "MARSHALL ISLANDS", "RI": "RHODE ISLAND", "KS": "KANSAS", "MT": "MONTANA", "MP": "NORTHERN MARIANA ISLANDS", "MS": "MISSISSIPPI", "PR": "PUERTO RICO", "SC": "SOUTH CAROLINA", "KY": "KENTUCKY", "OR": "OREGON", "SD": "SOUTH DAKOTA"}

# Org types to scrape
ORG_TYPES = ['police department', 'fire department', 'city hall', 'newspaper', 'tv station', 'hospital']

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
        pass
    try:
        Location.create_table() #only needed once
    except Exception, e:
        pass

def zipit():

    ifile  = open('zipcode.csv', "rb")
    reader = csv.reader(ifile)

    rownum = 0
    for row in reader:
        #ex: "zip","city","state","latitude","longitude","timezone","dst"

        # Fuck the header row.
        if rownum == 0:
            rownum+=1
            continue

        if len(row) < 7:
            print "Skipping " + str(row)
            continue

        has_loc = Location.select().where(Location.zip_code == row[0])
        has_loc = has_loc.execute()
        has_loc = [u for u in has_loc]

        if len(has_loc) > 0:
            print "Already have Location for zip: " + str(row[0])
            continue

        l = Location()
        l.zip_code = row[0]
        l.zip_code_string = str(row[0])
        l.city = slugify(row[1])
        l.state_code = row[2]
        l.state = slugify(code_to_state[row[2]])
        l.lat = row[3]
        l.lon = row[4]

        if l.lat is not "":
            l.save()
            print "Saved location: " + str(l) + ' ' + str(l.zip_code)

        rownum += 1

    ifile.close()

def check_locations():

    locations = Location.select().order_by(Location.zip_code.asc())
    locations = locations.execute()
    locations = [l for l in locations]

    for l in locations:
        print "Location: " + str(l.zip_code_string) + ' ' + l.city + ', ' + l.state 
    
    return

def scrape():

    # Where did we leave off?
    last_muni = Muni.select().order_by(Muni.zip_code.asc())
    last_muni = last_muni.execute()

    last_zip = 210
    try:
        for l in last_muni:
            last_zip = l.zip_code
    except Exception, e:
        print e
        last_zip = 210 #00210 is the lowest zip code. portsmouth, new-hampshire

    locations = Location.select().where(Location.zip_code>last_zip).order_by(Location.zip_code.asc())
    locations = locations.execute()

    for l in locations:
        print l.zip_code_string + ": " + l.city + ", " + l.state_code

        for org in ORG_TYPES:
            scrape_item_by_city_state_and_org(l.city, l.state_code, org, l.zip_code_string)


    return

def scrape_item_by_city_state_and_org(city, state, org, zipcode=None):

    time.sleep(3)

    try:

        print "Scraping " + org + " in " + city + ", " + state
        google_places = GooglePlaces(random.choice(GOOGLE_KEYS))

        results = google_places.query(
                    location= city + ", " + state, 
                    keyword=org,
                    )

        place = results.places[0]
        place.get_details()

        country = 'USA'
        state_code = state
        state_full = code_to_state[state]
        county = ''
        address = place.formatted_address
        url = place.website
        tel = place.local_phone_number
        international_tel = place.international_phone_number
        name = place.name
        lat = place.geo_location['lat']
        lon = place.geo_location['lng']

        print name
        print country
        print state_code
        print state_full
        print address
        print url
        print tel
        print lat
        print lon

        print '\n\n'

        m = Muni.create(    
                zip_code = zipcode,
                zip_code_string = zipcode,
                org = org,
                city = city,
                address = address,
                county = county,
                country=country,
                url = url,
                tel=tel,
                international_tel=international_tel,
                state_code = state_code,
                state = state_full,
                success = True,
                title = name,
                lat = lat,
                lon = lon,
                email = '',
                date_created = datetime.datetime.utcnow(),
                last_modified = datetime.datetime.utcnow()
            )

        return m

    except Exception, e:
        print e

        # SAVE FAILURE
        m = Muni.create(    
                zip_code = zipcode,
                zip_code_string = zipcode,
                org = org,
                city = city,
                state_code = state,
                state = code_to_state[state],
                success = False,
                country='USA',
                email = '',
                lat = '0',
                lon = '0',
                address = '',
                title = '',
                tel = '',
                international_tel = '',
                url = '',
                date_created = datetime.datetime.utcnow(),
                last_modified = datetime.datetime.utcnow(),
            )

        return m

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

def get_all_items():
    for m in Muni.select().where(Muni.success==True):
        print m.title + " " + str(m.tel)

setup_db()
#zipit()
#check_locations()
get_all_items()
scrape()
get_all_items()
