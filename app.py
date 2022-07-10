#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from email.policy import default
import json
import sys
import datetime
from unittest import result
from urllib import response
import dateutil.parser
import babel
import logging
from flask import Flask, render_template, request, Response, flash, redirect, session, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import Show, Venue, Artist, db
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  data=[]
  venues = Venue.query.all()
  locations = set()

  for venue in venues:
    locations.add((venue.city, venue.state))

  for location in locations:
    city_state={
      "city": location[0],
      "state": location[1],
      "venues": []
    }

  for venue in venues:
    for x in data:
      if x['city'] == venue.city and x['state'] == venue.state:
        venues = Show.query.join(Venue). filter(venue.id == venue.id),
        filter(Show.show_time > datetime.utcnow())
        new_venues = []
        for venue in venues:
          new_venues.append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len(list(filter(lambda x: x.start_time > datetime.now(), venue.show)))
          })

        city_state["venues"] = new_venues
        data.append(city_state)

    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  result = Venue.query.filter((Venue.name.ilike(f'%{search_term}%')) |
                              (Venue.city.ilike(f'%{search_term}%')) |
                              (Venue.state.ilike(f'%{search_term}%')))

  response={
    "count": result.count(),
    "data": result
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  venues = Venue.query.get(venue_id)
  upcoming_shows = Show.query.join(Venue).filter(Venue.id == venue_id).filter(Show.start_time > datetime.utcnow())
  past_shows = Show.query.join(Venue).filter(Venue.id == venue_id).filter(Show.start_time <= datetime.utcnow())

  return render_template('pages/show_venue.html', venue=venues, upcoming_shows=upcoming_shows,
                                                past_shows=past_shows)



#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm(request.form)
  block = form.data.get
  if form.validate():
    try: 
      venue = Venue(
        name = block('name'),
        city = block('city'),
        state = block('state'),
        address = block('address'),
        phone = block('phone'),
        image_link = block('image_link'),
        genres = block('genres'),
        facebook_link = block('facebook_link'),
        seeking_description = block('seeking_description'),
        website_link = block('website_link'),
        seeking_talent = block('seeking_talent')
      )

      db.session.add(venue)
      db.session.commit()

    # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    except:
      db.session.rollback()
      flash('An error occurred. Venue ' + request.form['name'] + ' Could not be listed')

    finally:
      db.session.close()

    return render_template('pages/home.html')
  else:
    flash('There is an error in the form, please fix and try again')
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  try:
    venue = Venue.query.get(venue_id)
    venue_name = venue.name

    db.session.delete(venue)
    db.session.commit()

    flash('Venue ' + venue_name + ' was deleted')

  except:
    flash('An error occured. Venue ' + venue_name + ' was not deleted')
    db.session.rollback()

  finally:
    db.session.close()

  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artist=[]

  artists = Artist.query.all()
  for artist in artists:
    artist.append({
      "id": artist.id,
      "name": artist.name,
    })
    
  return render_template('pages/artists.html', artists=artist)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  result = Artist.query.filter((Artist.name.ilike(f'%{search_term}%')) |
                               (Artist.city.ilike(f'%{search_term}%')) |
                               (Artist.state.ilike(f'%{search_term}%')))

  response={
    "count": result.count(),
    "data": result
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist = Artist.query.get(artist_id)
  upcoming_shows = Show.query.join(Artist).filter(Artist.id == artist_id).filter(Show.start_time > datetime.utcnow())
  past_shows = Show.query.join(Artist).filter(Artist.id == artist_id).filter(Show.start_time <= datetime.utcnow())

  return render_template('pages/show_artist.html', artist=artist, upcoming_shows=upcoming_shows,
                                                                  past_shows=past_shows)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)


  form.name.data = artist.name,
  form.genres.data = artist.genres,
  form.city.data = artist.city,
  form.state.data = artist.state,
  form.phone.data = artist.phone,
  form.facebook_link.data = artist.facebook_link,
  form.image_link.data = artist.image_link,
  form.website_link.data = artist.websit_link,
  form.seeking_venue.data = artist.seeking_venue,
  form.seeking_description.data = artist.seeking_description

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  if form.validate():
    try:
      artist.name = form.name.data
      artist.phone = form.phone.data
      artist.city = form.city.data
      artist.state = form.state.data
      artist.genres = form.genres.data
      artist.image_link = form.image_link.data
      artist.facebook_link = form.facebook_link.data
      artist.websit_link = form.website_link.data
      artist.seeking_venue = form.seeking_venue.data
      artist.seeking_description = form.seeking_description.data

      db.session.commit()
      flash('The Artist ' + request.form['name'] + 'has been successfully updated')

    except:
      db.session.rollback()
      flash('An Error has occured and update was unsucessful')

    finally:
      db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))
  else:
    flash('An Error has occured and update was unsucessful')
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)

  form.name.data = venue.name,
  form.genres.data = venue.genres,
  form.city.data = venue.city,
  form.state.data = venue.state,
  form.phone.data = venue.phone,
  form.facebook_link.data = venue.facebook_link,
  form.image_link.data = venue.image_link,
  form.website_link.data = venue.websit_link,
  form.seeking_talent.data = venue.seeking_talent,
  form.seeking_description.data = venue.seeking_description

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    name = VenueForm.name.data

    venue.name = name
    venue.genres = form.genres.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.address = form.address.data
    venue.phone = form.phone.data
    venue.facebook_link = form.facebook_link.data
    venue.website_link = form.website_link.data
    venue.image_link = form.image_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data

    db.session.commit()
    flash('Venue ' + name + 'has been updated')
  except:
    db.session.rollback()
    flash('An error occured while trying to update Venue')
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form)
  block = form.data.get
  if form.validate():
    try:
      artist = Artist(
        name=block('name'), 
        city=block('city'), 
        state=block('state'),
        phone=block('phone'),
        genres=block('genres'),
        image_link=block('image_link'),
        facebook_link=block('facebook_link'),
        website_link = block('website_link'),
        seeking_venue = block('seeking_venue'),
        seeking_description = block('seeking_description') 
        )
        
      db.session.add(artist)
      db.session.commit()
      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
      db.session.rollback()
      flash('An error ocurred, Artist ' + request.form['name'] + ' could not be listed')
    finally:
      db.session.close()
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')
  else:
    flash('There is an error in the form, please fix and try again')
    return render_template('pages/home.html')


@app.route('/artist/<int:artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  try:
    artist = Artist.query.get(artist_id)
    artist_name = artist.name

    db.session.delete(artist)
    db.session.commit()

    flash('Artist ' + artist_name + ' was deleted')
  except:
    flash('An error occured and Artist ' + artist_name + ' was not deleted')
    db.session.rollback()

  finally:
    db.session.close()
  return redirect(url_for('index'))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = Show.query.order_by(db.desc(Show.start_time))

  data = []
  for show in shows:
    data.append({
      'venue_id': show.venue_id,
      'artist_id': show.artist_id,
      'start_time': format_datetime(str(show.start_time))
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form)
  block = form.data.get
  if form.validate():
    try:
      show = Show(
        artist_id=block('artist_id'),
        venue_id=block('venue_id'),
        start_time=block('start_time')
        )

      db.session.add(show)
      db.session.commit()
      # on successful db insert, flash success
      flash('Show was successfully listed!')
    
    except:
      db.session.rollback()
      flash('An error occured. show could not be listed')
    finally:
      db.session.close()
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')
  else:
    flash('There is an error in the form, please fix and try again')
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
