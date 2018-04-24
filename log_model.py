from peewee import *

db = SqliteDatabase('worklogs.db')


class Log(Model):
    employee_name = CharField(max_length=255)
    task_name = CharField(max_length=255)
    date = CharField(max_length=10)
    time_spent = IntegerField()
    note = TextField()
    
    class Meta:
        database = db


def initialize():
    """Create the database and the table if they don't exist"""
    db.connect()
    db.create_tables([Log], safe=True)


