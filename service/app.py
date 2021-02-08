from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

db.init_app(app)
 
@app.before_first_request
def create_table():
    db.create_all()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'email')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


# endpoint to create new user
@app.route("/user", methods=["POST"])
def add_user():
    username = request.json['username']
    email = request.json['email']
    
    new_user = User(username, email)
    result = user_schema.dump(new_user)
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except: 
        return "Username or email already exists", '400'

    return jsonify(result)


# endpoint to show all users
@app.route("/user", methods=["GET"])
def get_user():
    try:
        all_users = User.query.all()
        if not all_users:
            raise 
    except:
        return "No data", '400'

    result = users_schema.dump(all_users)
    return jsonify(result)


# endpoint to get user detail by id
@app.route("/user/<id>", methods=["GET"])
def user_detail(id):
    try:
        user = User.query.get(id)
        if not users:
            raise 
    except: 
        return f"User with id: {id} does not exist", '400'
    return user_schema.jsonify(user)


# endpoint to update user
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)

    username = request.json['username']
    email = request.json['email']
    
    try:
        user.email = email
        user.username = username
        db.session.commit()
    except:
        return f"User with id: {id} does not exist", '400'
    
    return user_schema.jsonify(user)


# endpoint to delete user
@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
   
    try:
        db.session.delete(user)
        db.session.commit()
    except:
        return f"User with id: {id} does not exist", '400' 
    
    return user_schema.jsonify(user)


if __name__ == '__main__':
    app.run(debug=True)