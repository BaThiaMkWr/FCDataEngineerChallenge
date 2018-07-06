import requests
from urllib import urlencode
from flask import jsonify
from models.models import Real_Gross_Domestic_Product, University_of_Michigan_Customer_Sentiment_Index, US_Civilian_Unemployment_Rate
from runserver import app, db
from sqlalchemy import func
import datetime
from urllib import urlopen






def __fetch_data__(url):
    print

API_KEY = app.config.get('API_KEY')
API_URL = app.config.get('API_URL')

def model(series_id):

  if series_id == 'GDPC1' :
    return Real_Gross_Domestic_Product
  elif series_id == 'UMCSENT':
    return University_of_Michigan_Customer_Sentiment_Index
  elif series_id == 'UNRATE':
    return US_Civilian_Unemployment_Rate
  else:
    return None

# collect data since fred's api
def collect_observations(api_key, api_url, session, load_type="initial", **kwargs):

    url = api_url
    if kwargs.keys():
        url += '?' + urlencode(kwargs)
    url += "&api_key=" + api_key + "&file_type=json"

    response = requests.get(url)
    print response

    observations = [[observation["date"], observation["value"]] for observation in response.json()["observations"]]

    if load_type == "initial":
        return initialinsert(observations, model(kwargs["series_id"]), session)
    if load_type == "incremental":
        return incrementalinsert(observations, model(kwargs["series_id"]), session)
    else:
        return jsonify({"Error": "Unknow load type"})

#persist observations into database tables

# initial load ( delete & insert)
def initialinsert(observations, model, db):

    totalInserted = 0
    db.session.query(model).delete()
    db.session.commit()

    for observation in observations:
        date = observation[0]
        value = float(observation[1]) if observation[1] != '.' else None
        db.session.add(model(date, value))
        totalInserted += 1
    db.session.commit()
    return str(totalInserted)

#incremental (insert only none persist obs)
def incrementalinsert(observations, model, db):
    totalInserted = 0
    for observation in observations:
        date = observation[0]
        value = float(observation[1]) if observation[1] != '.' else None
        count = db.session.query(func.count(model.observation_date)).filter(model.observation_date == datetime.datetime.strptime(date, "%Y-%m-%d")).scalar()
        if int(count) == 0:
            db.session.add(model(date, value))
            totalInserted += 1
    db.session.commit()
    return str(totalInserted)

# process umployement rates
def unemploymentrates(db):

    query = """
        SELECT
          extract(year from observation_date) AS year,
          AVG(unemployment_rate) avg_unemployment_rate
        FROM series.us_civilian_unemployment_rate
        WHERE extract(year from observation_date)  >= 1980 AND extract(year from observation_date) <= 2015 
        GROUP BY extract(year from observation_date)
        ORDER BY extract(year from observation_date) DESC;
        """
    return db.engine.execute(query).fetchall()

#check if given param is allow base on this list
def check_params(given_params):
    expected_params = ["series_id", "file_type", "api_key","limit", "sort_order", "observation_start", "observation_end", "output_type", "vintage_dates"]
    for param in given_params:
        if param in expected_params:
            continue
        else:
            return False
    return True

def checkdataloads(db):

    query_ucur = """ SELECT to_char(observation_date, 'YYYYMMDD'), unemployment_rate FROM series.us_civilian_unemployment_rate LIMIT 5; """
    query_cmcsi = """ SELECT to_char(observation_date, 'YYYYMMDD'), sentiment_index  FROM series.University_of_Michigan_Customer_Sentiment_Index LIMIT 5; """
    query_rgdp = """ SELECT to_char(observation_date, 'YYYYMMDD'), rgdp_value FROM series.Real_Gross_Domestic_Product LIMIT 5; """

    return db.engine.execute(query_ucur).fetchall(), db.engine.execute(query_cmcsi).fetchall(), db.engine.execute(query_rgdp).fetchall()


def todict(data_array):
    data_array_dict = {}
    for data in data_array:
        data_array_dict[int(data[0])] = data[1]
    return data_array_dict


def load_data(load_type="initial", **kwargs):
    if kwargs:
        checkparams = check_params(kwargs.keys())
        if checkparams:
            if kwargs["series_id"] in ["GDPC1", "UMCSENT", "UNRATE"]:
                try:
                    totalInserted = collect_observations(API_KEY, API_URL, db, load_type, **kwargs)
                except:
                    return jsonify({'Error': 'Unable to collect data or to connect to the database. Please check your internet access or the given URL or database  access.'})
                return jsonify({
                    "Series": kwargs["series_id"],
                    "message": "Inserted " + totalInserted + " observations"
                })
            else:
                return jsonify({"Error": 'Series not supported. Please select one of GDPC1, UMCSENT, or UNRATE'})

        else:
            return jsonify({
                               "Error": 'Unsupported params. Please select one of  (series_id, file_type, api_key ,limit, sort_order, observation_start, observation_end, output_type, vintage_dates)'})

    else:
        return jsonify({"Error": 'Expect series_id as minimum arg'})

