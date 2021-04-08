# 1. imports
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# 2. Database setup
engine = create_engine("sqlite:///hawaii.sqlite")

# 3. reflect an existing database into a new model
Base = automap_base()
# and reflect the tables
Base.prepare(engine, reflect=True) 
# and save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# 4. Create an app, being sure to pass __name__
app = Flask(__name__)

# 5. Define name, location, and email
name = "Climate"
#location = "Houston"
#email = rice@mail.com

# 6. Define routes
@app.route("/")
def index():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #create session link from Python to the Database
    session = Session(engine)

    """Return a list of dates and precipitation"""
    # Query dates and precipitation
    precipitation = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    precip_dates = list(np.ravel(precipitation))

    return jsonify(precip_dates)

@app.route("/api/v1.0/stations")
def stations(): 

    #create session link from Python to the Database
    session = Session(engine)
    
    """Return a list of Stations"""
    #JSON list of stations
    station_info=session.query(Station).all()
    session.close()

    station_data = list(np.ravel(station_info))
    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():

    #create session link from Python to the Database
    session = Session(engine)
    
    """Return a JSON list of dates and temperature for the most active station over the last year of data"""

    #JSON data
    temp = session.query(Measurement)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    session = Session(engine)
    """Return a JSON list of minimum, maximum, and average temperature for a specific starting date"""
    query_start=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date>=start).all()

    session.close()

    start_data = list(np.ravel(query_start))
    return jsonify(start_data)

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    session = Session(engine)
    """Return a JSON list of minimum, maximum, and average temperature for a specific starting and end date"""
    query_start_end=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date>=start).filter(Measurement.date<=end).all()

    session.close()

    start_end_data = list(np.ravel(query_start_end))
    return jsonify(start_end_data)

if __name__ == '__main__':
    app.run(debug=True)