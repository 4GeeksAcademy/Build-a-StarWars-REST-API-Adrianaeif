"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200

#GET Users
@app.route('/user', methods=['GET'])
def info_user():

    user_list = User.query.all()
    response = [person.serialize() for person in user_list]

    return jsonify(response), 200


# CREATE User
@app.route('/user', methods=['POST'])
def add_user():
    body = request.json

    name = body.get('name', None)
    last_name = body.get('last_name', None)
    email = body.get('email',None)
    password = body.get('password', None)

    if name == None or last_name == None or email == None or password == None:
        return jsonify({"mg" : "Incompleto"}), 400

    try:

        new_user = User(name=name, last_name=last_name, email=email, password=password)
        db.session.add(new_user) 
        db.session.commit()
        
        return jsonify({"msg" : "Creado"}), 201

    except:
        return jsonify ({"Error" : "Incompleto"}), 500
    
# GET PEOPLE / CHARACTER
@app.route('/character', methods=['GET'])
def info_character():

    character_list = Character.query.all()
    response = [character.serialize() for character in character_list]

    return jsonify(response), 200
    

#GET ID CHARACTER

@app.route('/character/<int:id>', methods=['GET'])
def id_character(id):

    character = Character.query.get(id)
    if character == None:
        return jsonify({"msg" : "No se encontro"}), 400

    return jsonify(character.serialize()), 200


# GET PLANET
@app.route('/planets', methods=['GET'])
def info_planet():

    planet_list = Planet.query.all()
    response = [planet.serialize() for planet in planet_list]

    return jsonify(response), 200

#GET ID PLANET

@app.route('/planets/<int:id>', methods=['GET'])
def id_planet(id):

    planet = Planet.query.get(id)
    if planet == None:
        return jsonify({"msg" : "No se encontro"}), 400

    return jsonify(planet.serialize()), 200

#GET FAVORITE [/users/favorites]
@app.route('/users/<int:id>/favorites', methods=['GET'])
def user_favorite(id):

    favorites = Favorite.query.filter_by(user_id = id).all()

    favorites_serialize = [favorite.serialize() for favorite in favorites]

    return jsonify(favorites_serialize), 200

# POST Planet - User
@app.route('/user/<int:id>/favorite/planet/<int:planet_id>', methods = ['POST'])
def add_planet(id, planet_id):

    try:

        new_planet_favorite = Favorite(user_id = id, planet_id = planet_id)
        db.session.add(new_planet_favorite) 
        db.session.commit()
        
        return jsonify({"msg" : "success"}), 201

    except:
        return jsonify ({"Error" : "Error"}), 500

# POST Character - User
@app.route('/user/<int:id>/favorite/character/<int:character_id>', methods = ['POST'])
def add_character(id, character_id):

    try:

        new_character_favorite = Favorite(user_id = id, character_id = character_id)
        db.session.add(new_character_favorite ) 
        db.session.commit()
        
        return jsonify({"msg" : "success"}), 201

    except:
        return jsonify ({"Error" : "Error"}), 500
    
# DELETE Planet - User
@app.route('/user/<int:id>/favorite/planet/<int:planet_id>', methods = ['DELETE'])
def remove_planet(id, planet_id):

    searched_planet = Favorite.query.filter_by(user_id = id, planet_id = planet_id).one_or_none()

    if searched_planet != None:
        db.session.add(searched_planet) 
        db.session.commit()
        return jsonify(searched_planet.serialize()), 200

    else:
         return jsonify ({"Error" : "Error"}), 500
    

# DELETE Character - User
@app.route('/user/<int:id>/favorite/character/<int:character_id>', methods = ['DELETE'])
def remove_character(id, character_id):

    searched_character = Favorite.query.filter_by(user_id = id, character_id = character_id).one_or_none()

    if searched_character != None:
        db.session.add(searched_character) 
        db.session.commit()
        return jsonify(searched_character.serialize()), 200

    else:
         return jsonify ({"Error" : "Error"}), 500



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
