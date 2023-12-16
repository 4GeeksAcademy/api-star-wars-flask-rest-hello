from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }

class StarSystems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    number_of_planets = db.Column(db.Integer)
    galactic_coordinates = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return '<Starystems %r>' % self.starsystems

    def serialize(self):
        return {
            "id":  self.id,
            "name": self.name,
            "number_of_planets": self.number_of_planets,
            "galactic_coordiantes": self.galactic_coordinates
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    terrain = db.Column(db.String, nullable=False)
    climate = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.planets

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
            "climate": self.climate,
        }

class Species(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullabe=False)
    classification = db.Column(db.String, unique=True, nullabe=False)
    lifespan = db.Column(db.Integer)
    language = db.Column(db.String)

    def __repr__(self):
        return '<Species %r>' % self.species
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "classification": self.classification,
            "lifespan": self.lifespan,
            "language": self.language,
        }

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    birthdate = db.Column(db.Date)

    def __repr__(self):
        return '<Characters %r>' % self.characters
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "weight": self.weight,
            "birthdate": self.birthdate,
        }
    
class Factions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    leader = db.Column(db.String, unique=True, nullable=False)
    organization_type = db.Column(db.String)
    capital = db.Column(db.String)
    affiliation = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return '<Factions %r>' % self.factions
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "leader": self.leader,
            "organization_type": self.organization_type,
            "capital": self.capital,
            "affiliation": self.affiliation,
        }
    