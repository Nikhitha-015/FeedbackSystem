import hashlib
import os
from History_component.dao.feedback import FeedbackDao
from History_component.db import db
from History_component.models.image import Image
from History_component.schema.image import ImageSchema

class ImageProvider():
    @staticmethod
    def upload_image():
        import random
        image_folder = "D:/NikhithaAcharya/SB-Projects/History_component/images"
        try:
            image_files = [f for f in os.listdir(image_folder) if f.endswith((".png", ".jpg", ".jpeg"))]
            selected_image = random.choice(image_files)
            image_path = os.path.join(image_folder, selected_image)

            with open(image_path, "rb") as img_file:
                image_data = img_file.read()

            image_hash = hashlib.sha256(image_data).hexdigest()
            existing_image = Image.query.filter_by(image_hash=image_hash).first()
            if existing_image:
                return {"message": "Duplicate image already uploaded for another record"}, 400

            image_oid = FeedbackDao.insert_image_to_db(image_data)
            new_image = Image(
                images=image_oid,
                image_hash=image_hash
            )

            db.session.add(new_image)
            db.session.commit()

            return ImageSchema().dump(new_image), 200

        except Exception as e:
            print(f"Upload error: {e}")
            return {"message": "Internal server error"}, 500

    @staticmethod
    def upload_image_in_bytea():
        import random
        image_folder = "D:/NikhithaAcharya/SB-Projects/History_component/images"
        try:
            image_files = [f for f in os.listdir(image_folder) if f.endswith((".png", ".jpg", ".jpeg"))]
            selected_image = random.choice(image_files)
            image_path = os.path.join(image_folder, selected_image)
            with open(image_path, "rb") as img_file:
                image_data = img_file.read()
            image_hash = hashlib.sha256(image_data).hexdigest()
            existing_image = Image.query.filter_by(image_hash=image_hash).first()
            if existing_image:
                return {"message": "Duplicate image already uploaded for another record"}, 400
            new_image = Image(
                image_large_binary=image_data,
                image_hash=image_hash
            )
            db.session.add(new_image)
            db.session.commit()

            return ImageSchema().dump(new_image), 200

        except Exception as e:
            print(f"Upload error: {e}")
            return {"message": "Internal server error"}, 500