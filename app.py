from flask import Flask
from flask_cors import CORS
from routes import routes
from auth import login
from models import init_db

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST"]}})

init_db()

# login endpoint
app.add_url_rule('/api/login', view_func=login, methods=['POST'])

app.register_blueprint(routes)

app.run()