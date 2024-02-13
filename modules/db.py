from typing import Dict
from decouple import config

import psycopg2 as pg


class DB():
	def __init__(self):
		self.conn = pg.connect(host=config('DB_HOST'), database=config('DB_NAME'), user=config('DB_USER'), password=config('DB_PASSWORD'), port=config('DB_PORT'))
		self.cursor = self.conn.cursor()


	def __del__(self):
		self.conn.close()

	
	def register(self, username: str, password: str) -> int:
		self.cursor.execute("INSERT INTO users(username, password) VALUES (%s, %s) RETURNING id;", (username, password))
		self.conn.commit()

		return self.cursor.fetchone()[0]


	def get_user_by_username(self, username: str):
		self.cursor.execute("SELECT id, password FROM users WHERE username = %s;", (username,))
		user = self.cursor.fetchone()

		return user


	def get_user_by_id(self, id: int) -> Dict | None:
		self.cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
		user = self.cursor.fetchone()

		return user


	def create_task(self, description: str, user_id: int):
		self.cursor.execute("INSERT INTO tasks(description, user_id) VALUES (%s, %s) RETURNING id;", (description, user_id))
		self.conn.commit()

		return self.cursor.fetchone()[0]

	
	def get_task(self, task_id: int):
		self.cursor.execute("SELECT * FROM tasks WHERE id = %s;", (task_id,))
		task = self.cursor.fetchone()

		return task
	

	def get_tasks(self, user_id: int):
		self.cursor.execute("SELECT id, description FROM tasks WHERE user_id = %s;", (user_id,))
		tasks = self.cursor.fetchall()

		return tasks
	

	def update_task(self, task_id: int, user_id: int, description: str):
		self.cursor.execute("UPDATE tasks SET description = %s WHERE id = %s AND user_id = %s;", (description, task_id, user_id))
		self.conn.commit()


	def delete_task(self, task_id: int, user_id: int):
		self.cursor.execute("DELETE from tasks WHERE id = %s AND user_id = %s;", (task_id, user_id))
		self.conn.commit()
