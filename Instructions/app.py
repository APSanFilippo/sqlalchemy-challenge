import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_,distinct

from flask import Flask, jsonify



engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"Welcome!"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all date and precipitations"""
    # Query all passengers
    results = session.query(Measurement.date,Measurement.prcp).\
                order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    all_prcp = list(np.ravel(results))

    all_prcp = {all_prcp[i]: all_prcp[i + 1] for i in range(0, len(all_prcp), 2)} 

    
    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list og stations"""
    # Query all stations
    results = session.query(Station.station).\
                order_by(Station.station).all()

    session.close()

    all_station = list(np.ravel(results))

    return jsonify(all_station)


@app.route("/api/v1.0/tobs")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temp data for most active stations"""
    # Query all passengers
    results = session.query(Measurement.date,Measurement.tobs).\
                    filter(Measurement.station == 'USC00519281').\
                    filter(Measurement.date >= '2016-08-23').\
                    order_by(Measurement.date).all()

    session.close()
    
    all_temp = list(np.ravel(results))

    return jsonify(all_temp)

 


@app.route("/api/v1.0/<start>")
def start(date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, avg and max for an specific date"""
    # Query all tobs

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= date).all()

    session.close()

    return jsonify(results)


    
    # Create a dictionary from the row data and append to a list of start_date_tobs
    start_tob = []
    for min, avg, max in results:
        start_tob_dict = {}
        start_tob_dict["Min Temp"] = min
        start_tob_dict["Avg Temp"] = avg
        start_tob_dict["Max Temp"] = max
        start_tob.append(start_tob_dict) 
     
    return jsonify(start_tobs)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of Tmin, Tavg and Tmax tobs for an specific start and end dates"""
    # Query all tobs

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    
    # Create a dictionary from the row data and append to a list of start_end_date_tobs
    start_end_date = []
    for min, avg, max in results:
        start_end_date_dict = {}
        start_end_date_dict["Min Temp"] = min
        start_end_date_dict["Avg Temp"] = avg
        start_end_date_dict["Max Temp"] = max
        start_end_date.append(start_end_date_dict) 
    

    return jsonify(start_end_date)



if __name__ == '__main__':
    app.run(debug=True)