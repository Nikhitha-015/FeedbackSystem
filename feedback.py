from flask import request, Response, jsonify, session
from flask_login import login_required, current_user
from flask_restx import Namespace, Resource

from History_component.dao.feedback import FeedbackDao
from History_component.db import db
from History_component.providers.feedback import FeedbackProvider

feedback_ref=Namespace('feedback', strict_slashes=False)

@feedback_ref.route('/')
class FeedbackMain(Resource):
    @login_required
    def get(self):
        all_feedback=FeedbackProvider.get_feedback()
        return jsonify(all_feedback)

    @login_required
    def post(self):
        user_id=current_user.id
        if not user_id:
            return jsonify({"message": "User not authenticated"}), 401
        feedback_data = FeedbackProvider.create_feedback(user_id)
        return (feedback_data)



@feedback_ref.route('/image/<int:record_id>')
class FeedbackImageUpdate(Resource):

    @login_required
    def patch(self, record_id):
        updated_record = FeedbackProvider.upload_image(record_id)
        return updated_record

    @login_required
    def get(self,record_id):
        all_feedback = FeedbackDao.feedback_by_id(record_id)
        if not all_feedback or not all_feedback.images:
            return jsonify({"meesage":"Image not found"}), 404

        connection = db.session.connection().connection
        lo=connection.lobject(all_feedback.images,'rb')
        image_data=lo.read()
        connection.close()
        return Response(image_data, mimetype="image/jpeg")

@feedback_ref.route('/binaryimage/<int:record_id>')
class ImageUpload(Resource):
    @login_required
    def patch(self, record_id):
        updated_record = FeedbackProvider.upload_image_for_bytea(record_id)
        return updated_record


    @login_required
    def get(self,record_id):
        data=FeedbackDao.feedback_by_id(record_id)
        if data.image_large_binary is None:
            return jsonify({"meesage": "Image not found"}), 404
        image_data=data.image_large_binary
        return Response(image_data, mimetype="image/jpeg")