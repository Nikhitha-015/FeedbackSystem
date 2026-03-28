from marshmallow import Schema, fields

class ImageSchema(Schema):
    id=fields.Int(dump_only=True)
    image_description=fields.Int(dump_only=True)
    images = fields.Int(required=True)