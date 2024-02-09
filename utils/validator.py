from modules.db import DB


class Validator():
	def __init__(self) -> None:
		self.db = DB()


	def user_exists_by_id(self, id: int) -> bool:
		return bool(self.db.get_user_by_id(id))
	

	def user_exists_by_username(self, username: str) -> bool:
		return bool(self.db.get_user_by_username(username))


	def task_exists(id) -> bool:
		db = DB()
		db.cursor.execute("SELECT * FROM tasks WHERE id = %s", (id,))

		if len(db.cursor.fetchall()) > 0:
			return True

		return False
	

	def task_belongs_to_user(self, task_id: int, user_id: int):
		return bool(self.db.get_task(task_id, user_id))
