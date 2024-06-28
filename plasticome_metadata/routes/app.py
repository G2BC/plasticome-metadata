import os

from dotenv import load_dotenv
from flask import Flask, request
from flask_jwt_extended import JWTManager, jwt_required
from flask_pydantic_spec import FlaskPydanticSpec

from plasticome_metadata.controllers.enzyme_controller import (
    delete_enzyme,
    get_all_enzyme,
    get_enzyme,
    get_enzyme_by_ec,
    save_enzyme,
    update_enzyme,
)
from plasticome_metadata.controllers.plastic_controller import (
    delete_plastic,
    get_all_plastics,
    get_plastic,
    save_plastic,
    update_plastic,
)
from plasticome_metadata.controllers.plastic_enzyme_controller import (
    delete_plastic_enzyme,
    get_all_plastic_enzyme,
    get_plastic_enzymes,
    save_plastic_enzyme,
)
from plasticome_metadata.controllers.user_controller import authenticate_user
from plasticome_metadata.services.user_service import create_user

load_dotenv(override=True)

server = Flask(__name__)

server.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(server)

spec = FlaskPydanticSpec(
    'flask', title='PLASTICOME ENZYMES DEMO', version='v1.0', path='docs'
)
spec.register(server)


@server.post('/auth')
def user_auth():
    return authenticate_user(request.json)


@server.get('/enzyme_find')
@jwt_required(locations=['headers', 'cookies'])
def get_all_enzyme_route():
    return get_all_enzyme()


@server.get('/enzyme_find/<enzyme_id>')
@jwt_required(locations=['headers', 'cookies'])
def get_enzyme_route(enzyme_id):
    return get_enzyme(enzyme_id)


@server.get('/enzyme_find/ec/<ec_number>')
@jwt_required(locations=['headers', 'cookies'])
def get_enzyme_by_ec_route(ec_number):
    return get_enzyme_by_ec(ec_number)


@server.post('/enzyme_save')
@jwt_required(locations=['headers', 'cookies'])
def save_enzyme_route():
    return save_enzyme(request.json)


@server.patch('/enzyme_update/<int:id>')
@jwt_required(locations=['headers', 'cookies'])
def update_enzyme_route(id):
    data = request.json
    return update_enzyme(id, data)


@server.delete('/enzyme_delete/<int:id>')
@jwt_required(locations=['headers', 'cookies'])
def delete_enzyme_route(id):
    return delete_enzyme(id)


@server.get('/plastic_find')
@jwt_required(locations=['headers', 'cookies'])
def get_all_plastics_route():
    return get_all_plastics()


@server.get('/plastic_find/<acronym>')
@jwt_required(locations=['headers', 'cookies'])
def get_plastic_route(acronym):
    return get_plastic(acronym)


@server.post('/plastic_save')
@jwt_required(locations=['headers', 'cookies'])
def save_plastic_route():
    return save_plastic(request.json)


@server.patch('/plastic_update/<int:id>')
@jwt_required(locations=['headers', 'cookies'])
def update_plastic_route(id):
    data = request.json
    return update_plastic(id, data)


@server.delete('/plastic_delete/<int:id>')
@jwt_required(locations=['headers', 'cookies'])
def delete_plastic_route(id):
    return delete_plastic(id)


@server.get('/plastic_enzyme_find')
@jwt_required(locations=['headers', 'cookies'])
def get_all_plastic_enzymes_route():
    return get_all_plastic_enzyme()


@server.post('/plastic_enzyme_save')
@jwt_required(locations=['headers', 'cookies'])
def save_plastic_enzyme_route():
    return save_plastic_enzyme(request.json)


@server.get('/plastic_enzyme_find/<enzyme_id>')
@jwt_required(locations=['headers', 'cookies'])
def get_plastic_enzymes_route(enzyme_id):
    return get_plastic_enzymes(enzyme_id)


@server.delete('/plastic_enzyme_delete/<int:registered_id>')
@jwt_required(locations=['headers', 'cookies'])
def delete_plastic_enzyme_route(registered_id):
    return delete_plastic_enzyme(registered_id)

create_user('plasticome', 'admin')
server.run()
