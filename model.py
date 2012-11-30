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
    country = CharField(null=True)       
    state = CharField(null=True)
    state_code = CharField(null=True)     
    city = CharField(null=True)
    zip_code = FloatField(null=True)
    zip_code_string = CharField(null=True)
    lat = FloatField()
    lon = FloatField()
    address = CharField(null=True)

    # Contact information
    title = CharField(null=True)
    tel = CharField(null=True)
    international_tel = CharField(null=True)
    url = CharField(null=True)
    email = CharField(null=True)

    # Scrape info
    date_created = DateTimeField()
    last_modified = DateTimeField()

class Location(BaseModel):
    zip_code = IntegerField()
    zip_code_string = CharField()
    lat = FloatField()
    lon = FloatField()
    city = CharField() 
    state = CharField()
    state_code = CharField()

