from History_component.models import db


class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    user_prompt = db.Column(db.String(4098), nullable=False)
    response = db.Column(db.String(4098), nullable=False)
    feedback = db.Column(db.Boolean, nullable=True)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    image_large_binary = db.Column(db.LargeBinary, nullable=True)
    images = db.Column(db.Integer, unique=True, nullable=True)
    image_hash = db.Column(db.String(64), unique=True, nullable=True)
