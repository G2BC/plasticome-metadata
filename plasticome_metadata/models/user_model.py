from peewee import Model, CharField

from plasticome_metadata.models.config import database


class BaseModel(Model):
    class Meta:
        database = database


class PlasticomeUsers(BaseModel):
    username = CharField(unique=True)
    secret = CharField()


database.connect()
database.create_tables([PlasticomeUsers])
database.close()
