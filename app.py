from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:10203040@localhost:3306/flask"
app.secret_key = "sadasdsdssadsadsadsadsadssaddas"
db.init_app(app)

manager = LoginManager(app)
#https://www.youtube.com/watch?v=XUwOOqRDAHE&list=PLU2ftbIeotGrVZA85M6PnXSOHY7MnTBCc&index=4&ab_channel=letsCode

with app.app_context():
    from routes import *
    from models import User

    migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
