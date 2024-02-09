from decouple import config

import psycopg2 as pg


class DB():
	def __init__(self):
		self.conn = pg.connect(host=config('DB_HOST'), database=config('DB_NAME'), user=config('DB_USER'), password=config('DB_PASSWORD'), port=config('DB_PORT'))
		self.cursor = self.conn.cursor()


	def __del__(self):
		self.conn.close()


	def commit(self):
		self.conn.commit()


	def close(self):
		self.conn.close()


	def fetchone(self):
		return self.cursor.fetchone()


	def fetchall(self):
		return self.cursor.fetchall()