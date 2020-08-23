import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Base.classes.keys()

measurement = Base.classes.measurement
station = Base.classes.station
session= Session(engine)

# results = session.query(measurement.date, measurement.prcp).all()

# stations = session.query(station.station).all()



# results1 = session.query(measurement.date, measurement.tobs).filter(measurement.date>="2016-08-23").all()

# # print (session.query(func.min(measurement.tobs)).filter(measurement.date>="2016-08-23").all())
# # print (session.query(func.max(measurement.tobs)).filter(measurement.date>="2016-08-23").all())
# # print (session.query(func.avg(measurement.tobs)).filter(measurement.date>="2016-08-23").all())

# def calc_temps(start_date, end_date):
#     """TMIN, TAVG, and TMAX for a list of dates.
    
#     Args:
#         start_date (string): A date string in the format %Y-%m-%d
#         end_date (string): A date string in the format %Y-%m-%d
        
#     Returns:
#         TMIN, TAVE, and TMAX
#     """
    
#     return session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
#         filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()

# print(calc_temps("2016-08-23", "2017-08-23"))

app = Flask(__name__)

@app.route("/")
def welcome():
    print("Welcome to  'Home' page...")
    return "<h1>Welcome to the Climate App!</h1> </br>" + \
            "/api/v1.0/precipitation returns temperature observations from the past year</br>" + \
            "/api/v1.0/stations returns a json list of stations</br>" + \
            "/api/v1.0/tobs returns a json list of temperature observations from the last year</br>" + \
            "/api/v1.0/&ltstart&gt and /api/v1.0/&ltstart&gt/&ltend&gt returns a json list of min, avg, and max temp - given start or start-end range"

@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017,8,23)-dt.timedelta(365)

    precipitation = session.query(measurement.date, measurement.prcp).filter(measurement.date >= prev_year).all()

    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")
    stations = session.query(station.station).all()
    return jsonify(stations)         

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Temperature Observations (tobs)' page...")
    results1 = session.query(measurement.date, measurement.tobs).filter(measurement.date>="2016-08-23").all()
    return jsonify(results1)  

@app.route("/api/v1.0/<start>")
def temp(start):
    print("Server received request for dynamic temperature page with only start...")
    try: 
        #verify start date and end date are in the right format
        start_date = dt.datetime.strptime(start,"%Y-%m-%d")
        # end_date = date.today()
        
        #find matching dates from the previous year
        # prv_date = start_date-dt.timedelta(365)
        # post_date = end_date-dt.timedelta(365)
        
        # print("Searching for weather data from " + str(prv_date) + " to " + str(post_date))   
             
        results1 = session.query(measurement.date, measurement.tobs).filter(measurement.date>=start_date).all()    
                    
        df_weather = pd.DataFrame(data=results1,columns=["date","temp"])
        min_temp = df_weather["temp"].min()
        max_temp = df_weather["temp"].max()
        mean_temp = df_weather["temp"].mean()
        
        print("min_temp, mean_temp, and max_temp are returned")
        return jsonify({'TMIN': min_temp}, {'TAVG': mean_temp}, {'TMAX': max_temp})
        
    except:
        return "<p>input date is not in correct format. Dates should be formated as %Y-%m-%d</p>"
      

@app.route("/api/v1.0/<start>/<end>")
def temp_2(start,end):
    print("Server received request for dynamic temperature page with start and end...")
    try: 
        #start_date = dt.datetime.strptime(start,"%y-%m-%d")
        end_date = dt.datetime.strptime(end,"%Y-%m-%d")
        
        #prv_date = start_date-dt.timedelta(365)
        #post_date = end_date-dt.timedelta(365)
        
        #print("Searching for weather data from " + str(start_date) + " to " + str(end_date))
    
        results1 = session.query(measurement.date, measurement.tobs).filter(measurement.date>=end_date).all()
        
        df_weather = pd.DataFrame(data=results1,columns=["date","temp"])
        min_temp = df_weather["temp"].min()
        max_temp = df_weather["temp"].max()
        mean_temp = df_weather["temp"].mean()
        
        print("min_temp, mean_temp, and max_temp are returned")
        return jsonify({'TMIN':min_temp}, {'TAVG':mean_temp}, {'TMAX':max_temp})
        
    except:
        print("input dates are not in correct format. Dates should be formated as %Y-%m-%d")
    
if __name__ == "__main__":
    app.run()                   