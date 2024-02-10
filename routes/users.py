import json

from flask import Blueprint, request, Response
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest

from modules.db import DB
from utils.validator import Validator

users = Blueprint('users', __name__)
db = DB()
validator = Validator()


@users.route('/login', methods=['POST'])
def login():
	try:
		username = request.json.get('username')
		password = request.json.get('password')
	except BadRequest as e:
		return Response(status=400, response=json.dumps({'message': str(e)}), mimetype='application/json')

	if not username:
		return Response(status=422, response=json.dumps({'message': 'Username missing on request payload'}), mimetype='application/json')
	if not password:
		return Response(status=422, response=json.dumps({'message': 'Password missing on request payload'}), mimetype='application/json')

	user = db.get_user_by_username(username)

	if not user:
		return Response(status=404, response=json.dumps({'message': 'User not found.'}), mimetype='application/json')

	if not check_password_hash(user[1], password):
		return Response(status=403, response=json.dumps({'message': 'Invalid password.'}), mimetype='application/json')

	return Response(status=200, response=json.dumps({'userId': user[0], 'username': username}), mimetype='application/json')


@users.route('/register', methods=['POST'])
def register():
	username = request.json.get('username')
	password = request.json.get('password')
	hashed_password = generate_password_hash(password)

	if validator.user_exists_by_username(username):
		return Response(status=409, response=json.dumps({'message': 'Username already in use.'}), mimetype='application/json')

	user_id = db.register(username, hashed_password)

	return Response(status=200, response=json.dumps({'userId': user_id}), mimetype='application/json')
