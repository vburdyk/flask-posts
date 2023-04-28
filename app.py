from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

db = {
    'mysql_user': 'flask',
    'mysql_password': 'flask',
    'mysql_host': 'db:3306',
    'mysql_db': 'flask'
}

connection_str='mysql+pymysql://'+db['mysql_user']+':'+db['mysql_password']+'@'+db['mysql_host']+'/'+db['mysql_db']
app.config['SQLALCHEMY_DATABASE_URI']=connection_str

db = SQLAlchemy(app)

# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://flask:flask@db:3306/flask"
# app.secret_key = "sadasdsdssadsadsadsadsadssaddas"
# db.init_app(app)

manager = LoginManager(app)
#https://www.youtube.com/watch?v=XUwOOqRDAHE&list=PLU2ftbIeotGrVZA85M6PnXSOHY7MnTBCc&index=4&ab_channel=letsCode

with app.app_context():
    from routes import *
    from models import User

    migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
