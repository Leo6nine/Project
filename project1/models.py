
import datetime
from email.policy import default
from enum import unique
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique = True)
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120), nullable = False)
    address = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()), default = [])
    seeking_talent = db.Column(db.Boolean,  default = False)
    seeking_description = db.Column(db.String(800))
    Created_at = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    db.relationship('show', backref = 'venue', lazy = True)

    def __repr__(self):
       return f"<Venue id={self.id} name={self.name} city={self.city} state={self.state}>"
    # def __repr__(self):
    #     return f"<Venue id={self.id} name={self.name}>"

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique = True)
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()), default = [])
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default = False)
    seeking_description = db.Column(db.String(800))
    Created_at = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    db.relationship('show', backref = 'artist', lazy = True)

    def __repr__(self):
       return f"<Artist id={self.id} name={self.name}>"

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    start_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
       return f"<Show id={self.id} artist_id={self.artist_id} venue_id={self.venue_id} start_time={self.start_time}>"



# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.