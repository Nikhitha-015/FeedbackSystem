import hashlib
import os

from flask import jsonify, session
from flask import request, make_response

from History_component.dao.feedback import FeedbackDao
from History_component.db import db
from History_component.models import Feedback
from History_component.schema.feedback import FeedbackSchema


class FeedbackProvider:
    image_folder = "D:/NikhithaAcharya/SB-Projects/History_component/images"
    dummy_data = [{"user_prompt": "What is Python?",
                   "response": "It is a programming language used in web development, AI, datascience",
                   "feedback": None},
        {"user_prompt": "What is Python", "response": "It is a speaking language", "feedback": None},
        {"user_prompt": "Capital of India", "response": "Capital of India is Mumbai", "feedback": None},
        {"user_prompt": "Capital of India", "response": "Capital of India is New Delhi", "feedback": None},

    ]

    @staticmethod
    def get_feedback():
        feedback_data = FeedbackDao.get_feedback()
        response = FeedbackSchema(many=True)
        all_data = response.dump(feedback_data)

        return all_data

    def get_feedback_by_id(user_id):
        feedback_data = FeedbackDao.feedback_by_id(user_id)
        response = FeedbackSchema(many=False)
        all_data = response.dump(feedback_data)
        return all_data

    @staticmethod
    def create_feedback(user_id):
        import random
        image_folder = "D:/NikhithaAcharya/SB-Projects/History_component/images"
        feedback_text = request.args.get("feedback")
        feedback_bool = None
        if feedback_text:
            feedback_bool = feedback_text.lower() == "yes"
        if feedback_bool is None:
            import random
            random_data = random.choice(FeedbackProvider.dummy_data)
            user_prompt = random_data["user_prompt"]
            response = random_data["response"]
            session["user_prompt"] = user_prompt
            session["response"] = response
            return jsonify({"user_prompt": user_prompt, "response": response,
                "message": "Provide Feedback (True/False) before submitting."})
        user_prompt = session.get("user_prompt")
        response = session.get("response")
        if not user_prompt or not response:
            return make_response(jsonify({"message": "No data found. Please generate a prompt first."}), 400)
        image_data = None
        try:
            image_files = [f for f in os.listdir(image_folder) if f.endswith((".png", ".jpg", ".jpeg"))]
            if image_files:
                selected_image = random.choice(image_files)
                image_path = os.path.join(image_folder, selected_image)
                with open(image_path, "rb") as img_file:
                    image_data = img_file.read()
        except Exception as e:
            print(f"Error loading image: {e}")
        new_feedback = FeedbackDao.insert(user_prompt=user_prompt, response=response, user_id=user_id,
            feedback=feedback_bool, # images=image_data
        )
        session.pop("user_prompt", None)
        session.pop("response", None)
        final_data = FeedbackSchema().dump(new_feedback)
        return final_data

    @staticmethod
    def upload_image(record_id):
        import random
        image_folder = "D:/NikhithaAcharya/SB-Projects/History_component/images"
        try:
            image_files = [f for f in os.listdir(image_folder) if f.endswith((".png", ".jpg", ".jpeg"))]
            selected_image = random.choice(image_files)
            image_path = os.path.join(image_folder, selected_image)

            with open(image_path, "rb") as img_file:
                image_data = img_file.read()

            image_hash = hashlib.sha256(image_data).hexdigest()
            existing_image = Feedback.query.filter_by(image_hash=image_hash).first()
            if existing_image:
                return {"message": "Duplicate image already uploaded for another record"}, 400

            image_oid = FeedbackDao.insert_image_to_db(image_data)
            if not image_oid:
                return {"message": "Failed to store image"}, 500

            feedback = Feedback.query.get(record_id)
            feedback.images = image_oid
            feedback.image_hash = image_hash
            db.session.commit()

            return FeedbackSchema().dump(feedback), 200

        except Exception as e:
            print(f"Error loading image: {e}")
            return {"message": "Internal server error"}, 500

    def upload_image_for_bytea(record_id):
        import random
        image_folder = "D:/NikhithaAcharya/SB-Projects/History_component/images"
        try:
            image_files = [f for f in os.listdir(image_folder) if f.endswith((".png", ".jpg", ".jpeg"))]
            selected_image = random.choice(image_files)
            image_path = os.path.join(image_folder, selected_image)

            with open(image_path, "rb") as img_file:
                image_data = img_file.read()

                image_hash = hashlib.sha256(image_data).hexdigest()
                existing_image = Feedback.query.filter_by(image_hash=image_hash).first()
                if existing_image:
                    return {"message": "Duplicate image already uploaded for another record"}, 400

            feedback=Feedback.query.get(record_id)
            feedback.image_large_binary=image_data
            feedback.image_hash=image_hash
            db.session.commit()
            return {"message": f"Image uploaded successfully for record {record_id}"}, 200

        except Exception as e:
            return {"message": "Internal server error"}, 500
