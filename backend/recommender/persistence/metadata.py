from mongoengine import Document, StringField, DateTimeField


class Metadata(Document):
    date = DateTimeField(required=True)
    dataset_info = StringField(required=True)

