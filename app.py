# Step 2 - Climate App¶
# Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

# Use FLASK to create your routes.
# Routes
# /

# Home page.

# List all routes that are available.

# /api/v1.0/precipitation

# Convert the query results to a Dictionary using date as the key and prcp as the value.

# Return the JSON representation of your dictionary.

# /api/v1.0/stations

# Return a JSON list of stations from the dataset.
# /api/v1.0/tobs

# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.
# /api/v1.0/<start> and /api/v1.0/<start>/<end>

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

# Hints
# You will need to join the station and measurement tables for some of the analysis queries.

# Use Flask jsonify to convert your API data into a valid JSON response object.


import numpy as np
import pandas as pd
import datetime as dt 
import matplotlib.pyplot as plt 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite",connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return(
        f"Available Routes: <br>"

        f"/api/v1.0/precipitation<br/>"
        f"Returns dates and precipitaion from the last year. <br><br>"

        f"/api/v1.0/stations<br/>"
        f"Returns a json list of stations. <br><br>"

        f"/api/v1.0/tobs<br/>"
        f"Returns list of Temperature Observations(tobs) for previous year. <br><br>"

        f"/api/v1.0/<start><br/>"
        f"Returns Minimum, Average, and Maximum temperatures for a given start date (yyyy-mm-dd format).<br><br>"

        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
        f"Returns an Average, Max, and Min temperatures for a given range of start and end date (yyyy-mm-dd format)."
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-23", Measurement.date <= "2017-08-23").\
        all()

    precipitation_list = [results]
    return jsonify(precipitation_list)


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.name, Station.station, Station.elevation).all()

    station_list = []
    for result in results:
        row = {}
        row['name'] = result[0]
        row['station'] = result[1]
        row['elevation'] = result[2]
        station_list.append(row)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temp_obs():
    results = session.query(Station.name, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2016-08-23", Measurement.date <= "2017-08-23").\
        all()

    tobs_list = []
    for result in results:
        row = {}
        row["Station"] = result[0]
        row["Date"] = result[1]
        row["Temperature"] = int(result[2])
        tobs_list.append(row)
    return jsonify(tobs_list)

@app.route('/api/v1.0/<start>/')
def given_date(start):
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    start_date_list = []
    for result in results:
        row = {}
        row['Start Date'] = start
        row['End Date'] = '2017-08-23'
        row['Average Temperature'] = float(result[0])
        row['Highest Temperature'] = float(result[1])
        row['Lowest Temperature'] = float(result[2])
        start_date_list.append(row)
    return jsonify(start_date_list)

@app.route('/api/v1.0/<start_date>/<end_date>/')
def query_dates(start_date, end_date):
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    dates_list = []
    for result in results:
        row = {}
        row["Start Date"] = start_date
        row["End Date"] = end_date
        row["Average Temperature"] = float(result[0])
        row["Highest Temperature"] = float(result[1])
        row["Lowest Temperature"] = float(result[2])
        dates_list.append(row)
    return jsonify(dates_list)

if __name__ == '__main__':
    app.run(debug=True)

