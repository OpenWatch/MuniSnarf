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

def get_all_items():
    for m in Muni.select().where(Muni.success==True):
        print m.title + " " + str(m.tel)

setup_db()
get_all_items()
