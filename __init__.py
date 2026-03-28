from flask import Blueprint
from flask_restx import Api

from History_component.endpoint.feedback import feedback_ref
from History_component.endpoint.user import user_login
from History_component.endpoint.image import image
API_BLUEPRINT = Blueprint('api', __name__, url_prefix='/api/demo')

API = Api(
    API_BLUEPRINT,
    default="Feedback POC",
    title='Demo Project',
    )

API.add_namespace(feedback_ref)
API.add_namespace(user_login)
API.add_namespace(image)