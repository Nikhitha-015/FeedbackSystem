import base64
from History_component.db import db
from History_component.models.image import Image

class ImageDao:

    @staticmethod
    def image_by_id(record_id):
        return Image.query.filter(Image.id==record_id).first()