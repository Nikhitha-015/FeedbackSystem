from History_component.models import db


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    image_description=db.Column(db.Text, nullable=True)
    image_large_binary = db.Column(db.LargeBinary, nullable=True)
    images = db.Column(db.Integer, unique=True, nullable=True)
    image_hash = db.Column(db.String(64), unique=True, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)