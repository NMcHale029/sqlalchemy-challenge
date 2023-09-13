# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, text
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite",
                       connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert the query results from precipitation analysis (last 12 months) to a dictionary
    # sets the query date and uses that date to set the date for a year ago
    query_date = dt.date(2017, 8, 23)
    one_year_ago = query_date - dt.timedelta(days=365)
    # Queries date and perciptiation for the last year, orderd by date
    last_12_months = session.query(measurement.date, measurement.prcp)\
        .filter(measurement.date >= one_year_ago)\
        .order_by(measurement.date.desc()).all()

    session.close()

    # Set an empty dictionary to put data into
    prcp_dict = {}

    # Loops through the data pulled from the above query to populate the dictionary
    for row in last_12_months:
        prcp_dict[row['date']] = row['prcp']

    # Return a JSON list of stations from the dataset
    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():

    station_info = session.query(station.station).all()
    station_info = list(np.ravel(station_info))

    # Return a JSON lis of stations from the dataset
    return jsonify(station_info)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the dates and temperature observations of the most-active station for the previous year of data
    query_date = dt.date(2017, 8, 23)
    one_year_ago = query_date - dt.timedelta(days=365)
    temps = session.query(measurement.date, measurement.tobs)\
        .filter(measurement.station == 'USC00519281')\
        .filter(measurement.date >= one_year_ago).all()

    session.close()

    temps = list(np.ravel(temps))

    # Return a JSON list of temperature observations for the previous year
    return jsonify(temps=temps)


@app.route("/api/v1.0/<start>")
def begining(start=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query temperature observations from a given start date to the end of the data set
    print('Please indicate from which date you would like temperature data:')
    # year = input('From what year? ')
    # month = input('From what month? ')
    # day = input('From what day? ')

    query_date = dt.datetime.strptime(start, "%m%d%Y")

    # temp_data = engine.execute(text(f'SELECT MIN(tobs), MAX(tobs), AVG(tobs)\
    # FROM measurement\
    # WHERE date >= {query_date}')).all()
    select = [func.min(measurement.tobs), func.max(
        measurement.tobs), func.avg(measurement.tobs)]
    temp_data = session.query(
        *select).filter(measurement.date >= query_date).all()

    session.close()

    # Returns the min, max, and average temperatures calculated from
    # the given start date to the end of the dataset
    temp_data = list(np.ravel(temp_data))

    return jsonify(temp_data=temp_data)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Accepts the start and end dates as parameters

    start_date = dt.datetime.strptime(start, "%m%d%Y")
    end_date = dt.datetime.strptime(end, "%m%d%Y")

    # Queries the min, max, and average of observed temperature in the selected timeframe.
    select = [func.min(measurement.tobs), func.max(
        measurement.tobs), func.avg(measurement.tobs)]
    temp_data = session.query(*select).filter(measurement.date >= start_date)\
        .filter(measurement.date <= end_date).all()

    session.close()

    # Returns the min, max, and average temperatures calculated from
    # the given start date to the end of the dataset
    temp_data = list(np.ravel(temp_data))

    return jsonify(temp_data=temp_data)


if __name__ == '__main__':
    app.run(debug=True)
