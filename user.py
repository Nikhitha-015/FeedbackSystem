from flask_login import UserMixin

from History_component.models import db

class User(db.Model, UserMixin):
    __tablename__="users"
    name=db.Column(db.String(250), nullable=False)
    email_id=db.Column(db.String(250), nullable=False, unique=True)
    id=db.Column(db.Integer, primary_key=True)
    created_at=db.Column(db.DateTime(), nullable=False, server_default=db.func.current_timestamp())
    feedback=db.relationship("Feedback", backref="user")
