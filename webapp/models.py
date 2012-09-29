from core import peewee
from core import settings
from flask.ext import admin
from flask.ext.admin.contrib import peeweemodel
import sqlite3

db = peewee.SqliteDatabase(settings.DATABASE_NAME, check_same_thread=False)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Person(BaseModel):
    name = peewee.CharField(max_length=80)


class User(Person):
    email = peewee.CharField(max_length=120)
    password = peewee.CharField(max_length=250)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __unicode__(self):
        return self.email


class InventoryItem(BaseModel):
    name = peewee.CharField(max_length=255)
    identifier = peewee.CharField(unique=True, null=True, max_length=500)
    comment = peewee.CharField(null=True, max_length=200)
    date_added = peewee.DateTimeField(null=True)


class InventoryLog(BaseModel):
    status = peewee.CharField(choices=['Checkin', 'Checkout'])
    date_mod = peewee.DateTimeField()


def setup():
    tables = (User,)
    for table in tables:
        try:
            table.create_table()
            if User == table:
                # add an admin user
                User.insert(
                    name='admin',
                    email='admin@example.com',
                    password='admin'
                ).execute()
                pass
        except sqlite3.OperationalError:
            # table may already exist
            pass
