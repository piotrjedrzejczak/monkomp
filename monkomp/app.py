from flask import Flask
from database import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\dev\\repos\\monkomp\\data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    db.create_all(app=app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)