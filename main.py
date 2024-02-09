from flask import Flask
from flask_cors import CORS

from routes.tasks import tasks
from routes.users import users
from utils.validator import Validator

app = Flask(__name__)
CORS(app)
validator = Validator()

app.register_blueprint(users)
app.register_blueprint(tasks)

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)