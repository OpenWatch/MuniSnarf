from peewee import *

DATABASE = 'muni.db'
database = SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta:
        database = database

class Muni(BaseModel):

    # Meta information
    verified = BooleanFalse(default=False) # Has this been human-checked?
    success = BooleanFalse(default=False) # Was the scrape a success?

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
    url = CharField()
    email = CharField()

    # Scrape info
    date_created = DateTimeField()
    last_modified = DateTimeField()

class Location(models.Model):
    zip_code = models.IntegerField()
    lat = models.FloatField()
    lon = models.FloatField()
    city = models.CharField() 
    state = models.CharField()
    state_code = models.CharField()