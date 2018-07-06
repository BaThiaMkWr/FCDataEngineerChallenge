from runserver import app
from flask import jsonify, request
from models.models import db
from utils.utils import unemploymentrates, checkdataloads, todict, load_data


# initial load
@app.route("/initial_load",  methods=['GET'])
def initial_load():
  kwargs = request.args.to_dict()
  print kwargs
  return load_data(**kwargs)

# incremental load
@app.route("/incremental_load",  methods=['GET'])
def incremental_load():
  kwargs = request.args.to_dict()
  return load_data("incremental", **kwargs)

# unemployment rates
@app.route('/unemployment_rates', methods=['GET'])
def unemployment_rates():
      return jsonify(todict(unemploymentrates(db)))


@app.route('/check_data_loads', methods=['GET'])
def check_data_loads():
    ucur, umcsi, rgdp = checkdataloads(db)
    return jsonify({"US_Civilian_Unemployment_Rate":todict(ucur),
                    "University_of_Michigan_Customer_Sentiment_Index": todict(umcsi),
                    "Real_Gross_Domestic_Product": todict(rgdp)})


# not found page
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"Error": str(error)})

# wrong error
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"Error": str(error)})

