import json

from flask import Blueprint, request, Response

from modules.db import DB
from utils.validator import Validator

tasks = Blueprint('tasks', __name__)
db = DB()
validator = Validator()


@tasks.route('/create_task', methods=['POST'])
def create_task():
	user_id = request.json.get('userId')
	description = request.json.get('description')

	if not validator.user_exists_by_id(user_id):
		return Response(status=404, response=json.dumps({'message': 'User not found.'}), mimetype='application/json')

	db.create_task(description, user_id)

	return Response(status=200)


@tasks.route('/delete_task', methods=['DELETE'])
def delete_task():
	task_id = request.json.get('taskId')
	user_id = request.json.get('userId')

	if not user_id:
		return Response(status=422, response=json.dumps({'message': 'User ID missing on request payload'}), mimetype='application/json')

	if not task_id:
		return Response(status=422, response=json.dumps({'message': 'Task ID missing on request payload'}), mimetype='application/json')

	if not validator.user_exists_by_id(user_id):
		return Response(status=404, response=json.dumps({'message': 'User not found'}), mimetype='application/json')

	task = db.get_task(task_id)

	if not task:
		return Response(status=404, response=json.dumps({'message': 'Task not found'}), mimetype='application/json')
	
	if not validator.task_belongs_to_user(task_id, user_id):
		return Response(status=403, response=json.dumps({'message': 'Task not assigned to user'}), mimetype='application/json')

	db.delete_task(task_id, user_id)

	return Response(status=200)


@tasks.route('/update_task', methods=['PATCH'])
def update_task():
	task_id = request.json.get('taskId')
	user_id = request.json.get('userId')
	description = request.json.get('description')

	if not user_id:
		return Response(status=422, response=json.dumps({'message': 'User ID missing on request payload'}), mimetype='application/json')

	if not task_id:
		return Response(status=422, response=json.dumps({'message': 'Task ID missing on request payload'}), mimetype='application/json')
	
	if not description:
		return Response(status=422, response=json.dumps({'message': 'Description missing on request payload'}), mimetype='application/json')

	task = db.get_task(task_id)

	if not task:
		return Response(status=404, response=json.dumps({'message': 'Task not found'}), mimetype='application/json')
	
	if not validator.task_belongs_to_user(task_id, user_id):
		return Response(status=403, response=json.dumps({'message': 'Task not assigned to user'}), mimetype='application/json')

	if not validator.task_belongs_to_user(task_id, user_id):
		return Response(status=403, response=json.dumps({'message': 'Task not assigned to user'}), mimetype='application/json')

	db.update_task(description, task_id)

	return Response(status=200)


@tasks.route('/get_task', methods=['GET'])
def get_task():
	user_id = request.args.get('userId')
	task_id = request.args.get('taskId')

	if not user_id:
		return Response(status=422, response=json.dumps({'message': 'User ID missing on request payload'}), mimetype='application/json')

	if not task_id:
		return Response(status=422, response=json.dumps({'message': 'Task ID missing on request payload'}), mimetype='application/json')

	if not validator.user_exists_by_id(user_id):
		return Response(status=404, response=json.dumps({'message': 'User not found'}), mimetype='application/json')

	task = db.get_task(task_id)

	if not task:
		return Response(status=404, response=json.dumps({'message': 'Task not found'}), mimetype='application/json')
	
	if not validator.task_belongs_to_user(task_id, user_id):
		return Response(status=403, response=json.dumps({'message': 'Task not assigned to user'}), mimetype='application/json')

	return Response(status=200, response=json.dumps({'id': task[0], 'description': task[1]}), mimetype='application/json')


@tasks.route('/get_tasks', methods=['GET'])
def get_tasks():
	user_id = request.args.get('userId')

	if not user_id:
		return Response(status=422, response=json.dumps({'message': 'User ID missing on request payload'}), mimetype='application/json')

	if not validator.user_exists_by_id(user_id):
		return Response(status=404, response=json.dumps({'message': 'User not found'}), mimetype='application/json')

	tasks = db.get_tasks(user_id)

	return Response(status=200, response=json.dumps([{'id': task[0], 'description': task[1]} for task in tasks]), mimetype='application/json')
