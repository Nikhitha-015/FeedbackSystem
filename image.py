from flask import request, Response, jsonify, session
from flask_login import login_required
from flask_restx import Namespace, Resource

from History_component.dao.image import ImageDao
from History_component.db import db
from History_component.providers.image import ImageProvider

image=Namespace('images', strict_slashes=False)

@image.route('/upload')
class ImageUpdate(Resource):

    @login_required
    def post(self):
        updated_record = ImageProvider.upload_image()
        return updated_record

@image.route('/<int:record_id>')
class ImageRetreive(Resource):

    @login_required
    def get(self,record_id):
        all_data = ImageDao.image_by_id(record_id)
        if not all_data or not all_data.images:
            return jsonify({"meesage":"Image not found"}), 404

        connection = db.session.connection().connection
        lo=connection.lobject(all_data.images,'rb')
        image_data=lo.read()
        connection.close()
        return Response(image_data, mimetype="image/jpeg")

@image.route('/binaryimage/')
class ImageUpload(Resource):

    @login_required
    def post(self):
        updated_record = ImageProvider.upload_image_in_bytea()
        return updated_record

@image.route('/binary_image/<int:record_id>')
class ImageRetreive(Resource):

    @login_required
    def get(self,record_id):
        data=ImageDao.image_by_id(record_id)
        if data.image_large_binary is None:
            return jsonify({"message": "Image not found"}), 404
        image_data=data.image_large_binary
        return Response(image_data, mimetype="image/jpeg")