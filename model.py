from peewee import *

DATABASE = 'muni.db'
database = SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta:
        database = database

class Muni(BaseModel):

    # Meta information
    verified = BooleanField(default=False) # Has this been human-checked?
    success = BooleanField(default=False) # Was the scrape a success?

    # ex: 'police', 'fire', 'city hall', 'newspaper', 'tv station', 'hospital'
    org = CharField()

    # Location information
    country = CharField()       
    state = CharField()
    state_code = CharField()     
    county = CharField()
    city = CharField()
    zip_code = FloatField()
    lat = FloatField()
    lon = FloatField()
    address = CharField()

    # Contact information
    title = CharField()
    tel = CharField()
    international_tel = CharField()
    url = CharField()
    email = CharField()

    # Scrape info
    date_created = DateTimeField()
    last_modified = DateTimeField()

class Location(BaseModel):
    zip_code = IntegerField()
    lat = FloatField()
    lon = FloatField()
    city = CharField() 
    state = CharField()
    state_code = CharField()