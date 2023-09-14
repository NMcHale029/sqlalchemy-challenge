# sqlalchemy-challenge

### Dependencies
%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as st
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, text
import datetime as dt
from flask import Flask, jsonify


### Climate Starter
After creating a connection to an sqlite database, the last date of data collection was found. That date was used to identify the timeframe for the last year's worth of data. Data was then plotted and queried.

### app
When running the app, there are 5 routes you can take:
1. /api/v1.0/precipitation: This shows the date and percipitation from that date for every day for a year.
2. /api/v1.0/stations: This shows a list of stations
3. /api/v1.0/tobs: Temperatures observed on for every day for a year.
4. /api/v1.0/: In the URL you can enter a date in this formatt "MM-DD-YYYY" and the page will return the the min, max, and average tempurature for the dates between the date given in the URL and the last date that data was collected (08-23-2017).
5. /api/v1.0//: In the URL you can enter two dates in this formatt "MM-DD-YYYY/MM-DD-YYYY" and the page will return the the min, max, and average tempurature for the dates between the first date given and last date given in the URL.