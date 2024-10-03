from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __init__ (self, name, last_name, email, password):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_active = True

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=False)
    mass = db.Column(db.Float, nullable=False)
    unit_heigth = db.Column(db.String(250), nullable=False)
    unit_mass = db.Column(db.String(250), nullable=False)

    def __init__ (self, name, heigth, mass, unit_heigth, unir_mass):
        self.name = name
        self.height = heigth
        self.mass = mass
        self.unit_heigth = unit_heigth
        self.unit_mass = unir_mass

    def __repr__(self):
        return '<Character %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    surface_water= db.Column(db.Integer, nullable=False)
    diameter= db.Column(db.Integer, nullable=False)

    def __init__ (self, name, climate, population, rotation_period, surface_water, diameter):
        self.name = name
        self.climate = climate
        self.population = population
        self.rotation_period = rotation_period
        self.surface_water = surface_water
        self.diameter = diameter

    def __repr__(self):
        return '<Planet %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    
class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship(User)
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"))
    character = db.relationship(Character)
    planet_id  = db.Column(db.Integer, db.ForeignKey("planet.id"))
    planet = db.relationship(Planet)


    def __init__(self, id, user_id, character_id, planet_id ):
         self.id = id
         self.user_id = user_id
         self.character_id = character_id
         self.planet_id = planet_id 

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        return {
            "id" : self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
        }