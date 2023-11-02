from mongoengine import Document, StringField, ListField


class Endpoint(Document):
    endpoint = StringField(required=True)
    description = StringField(required=True)
    bow = ListField()

