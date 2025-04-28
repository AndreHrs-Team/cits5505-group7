from flask import Flask

app = Flask(__name__,
            static_folder="../frontend/static",
            static_url_path="/assets",
            template_folder="../frontend/templates")

from routes import init_routes
init_routes(app)

if __name__ == '__main__':    
    app.run(debug=True) #debug mode for live reload, only works with python app.py