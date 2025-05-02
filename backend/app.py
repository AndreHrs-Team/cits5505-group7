from flask import Flask
from models import init_models
from config import Config
from extensions import init_db

from routes import init_routes
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__,
            static_folder="../frontend/static",
            static_url_path="/assets",
            template_folder="../frontend/templates")
app.config.from_object(Config)
init_db(app)
init_models()
init_routes(app)

if __name__ == '__main__':
    # debug mode for live reload, only works with python app.py
    app.run(debug=True)
