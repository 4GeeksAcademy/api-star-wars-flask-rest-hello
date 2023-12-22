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
from models import db, User, Star_Systems, Factions, Planets, Species, Characters, User_Favorite
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

@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    serialized_users = [User.serialize() for User in users]
    return({'msg': 'Here you go all the users currently in the database', 'result': serialized_users}), 200

@app.route('/characters', methods=['GET'])
def get_characters():
    character = Characters.query.all() 
    serialized_characters = [Characters.serialize() for Characters in character] 
    return({'msg': 'Here you go all the people currently in the database', 'result': serialized_characters}), 200 

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planets.query.all()
    serialized_all_planets = [Planets.serialize() for Planets in all_planets]
    return({'msg': 'Here you go all the planets currently in the database', 'result': serialized_all_planets}), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_one_person(character_id):
    character = Characters.query.get(character_id)
    return jsonify({'msg': 'Here you go the person', 'result': character.serialize()}), 200
    
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planets.query.get(planet_id)
    return jsonify({'msg': 'Here you go the planet', 'result': planet.serialize()}), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    current_user_id = get_current_user_id()
    user_favorites = User_Favorite.query.filter_by(user_Id= current_user_id).all()
    serialized_favorites = [favorite.serialize() for favorite in user_favorites]
    return {'msg': 'Here are the favorites for the current user', 'result': serialized_favorites}, 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
     current_user_id = get_current_user_id()
     existing_favorite = User_Favorite.query.filter_by(user_Id=current_user_id, planet_Id=planet_id).first()
     if existing_favorite:
            return {'msg': 'Favorite planet already exists for the current user'}, 400
     new_favorite = User_Favorite(user_Id=current_user_id, planet_Id=planet_id, name_of_favorite='planet')
     db.session.add(new_favorite)
     db.session.commit()
     return {'msg': 'Favorite planet added successfully'}, 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
     current_user_id = get_current_user_id()
     existing_favorite = User_Favorite.query.filter_by(user_Id=current_user_id, character_Id=people_id_id).first()
     if existing_favorite:
            return {'msg': 'Favorite planet already exists for the current user'}, 400
     new_favorite = User_Favorite(user_Id=current_user_id, character_Id=people_id, name_of_favorite='people')
     db.session.add(new_favorite)
     db.session.commit()
     return {'msg': 'Favorite people added successfully'}, 201
        

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
     current_user_id = get_current_user_id()
     favorite_planet = User_Favorite.query.filter_by(user_Id=current_user_id, planet_Id=planet_id).first()
     if not favorite_planet: 
        return {'msg': 'Favorite planet not found for the current user'}, 404
     db.session.delete(favorite_planet)
     db.session.commit()
     return {'msg': 'Favorite planet deleted successfully'}, 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
     current_user_id = get_current_user_id()
     favorite_person = User_Favorite.query.filter_by(user_Id=current_user_id, character_Id=people_id).first()
     if not favorite_person: 
        return {'msg': 'Favorite person not found for the current user'}, 404
     db.session.delete(favorite_person)
     db.session.commit()
     return {'msg': 'Favorite person deleted successfully'}, 200

def get_current_user_id():
    return 1

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
