from peewee import Model, CharField, TextField, ForeignKeyField

from plasticome_metadata.models.config import database


class BaseModel(Model):
    class Meta:
        database = database


class PlasticTypes(BaseModel):
    plastic_name = CharField()
    acronym = CharField()


class EnzymeMetadata(BaseModel):
    cazy_family = CharField(null=True)
    fungi_name = CharField(null=True)
    enzyme_name = CharField()
    ec_number = CharField(null=True)
    protein_sequence = TextField(null=True)
    article_doi = CharField(null=True)
    genbank_protein_id = CharField(null=True)


class EnzymePlasticTypes(BaseModel):
    enzyme_id = ForeignKeyField(EnzymeMetadata, backref='enzyme_plastic_types')
    plastic_id = ForeignKeyField(
        PlasticTypes, backref='plastic_associated_enzymes'
    )


database.connect()
database.create_tables([PlasticTypes, EnzymeMetadata, EnzymePlasticTypes])
database.close()
