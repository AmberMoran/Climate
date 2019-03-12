import numpy as np
import datetime as dt
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
	return(
		f"Hawaii Climate Analysis API<br/>"
		f"Available Routes:<br/>"
		F"/api/v1.0/precipitation<br/>"
		f"/api/v1.0/stations<br/>"
		f"/api/v1.0/tobs<br/>"
		f"/api/v1.0/start<br/>"
		f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
   last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

   rain = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > last_year).\
        order_by(Measurement.date).all()

   rain_totals = []
   for result in rain:
        row = {}
        row["date"] = rain[0]
        row["prcp"] = rain[1]
        rain_totals.append(row)

   return jsonify(rain_totals)


@app.route("/api/v1.0/stations")
def stations():
   results = session.query(Station.station,Station.name).all()

   stations = []
   for result in results:
        row = {}
        row["station"] = results[0]
        row["name"] = results[1]
        stations.append(row)

   return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
   last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

   temperature = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > last_year).\
        order_by(Measurement.date).all()

   temps =[]
   for result in temperature:
        row = {}
        row["date"] = temperature[0]
        row["tobs"] = temperature[1]
        temps.append(row)

   return jsonify(temps)

@app.route("/api/v1.0/start")
def start(start=None):
   startdate = dt.date(2017,3,1)

   results =  session.query(Measurement.date,func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    group_by(Measurement.date).filter(Measurement.date>=startdate).all()

   temp_date = list(np.ravel(results))

   trip = []
   for result in results:
      row = {}
      row["date"] = result[0]
      row["min"] = result[1]
      row["avg"] = result[2]
      row["max"] = result[3]
      trip.append(row)

      
   return jsonify(trip)


@app.route("/api/v1.0/start/end")
def temp_start_end():
   startdate = dt.date(2017,3,1)
   enddate = dt.date(2017,3,12)

   results2 =  session.query(Measurement.date,func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
    group_by(Measurement.date).filter(Measurement.date.between(startdate,enddate)).all()

   #trip2 = list(np.ravel(results2))

   vacation = []
   for result in results2:
    row = {}
    row["date"] = result[0]
    row["min"] = result[1]
    row["avg"] = result[2]
    row["max"] = result[3]
    vacation.append(row)
   
   return jsonify(vacation)
  
if __name__ == '__main__':
    app.run(debug=True)
