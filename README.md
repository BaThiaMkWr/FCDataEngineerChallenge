###FC Data Engineering Coding Challenge
This Flask app collects and loads data from the FRED api's GDPCI, UMC Sentiment Index, and Unemployment rate series.
Introduction
For this exercise, we would like you to build a simple application for pulling and storing different kinds of macro-economic data using the Federal Reserve’s FRED API.
The FRED API provides a RESTful means of accessing many datasets published by the Federal Reserve – unemployment rates, interest rates, GDP etc.
The data is modelled as a ‘series’ of ‘observations’ with each observation having a date and value.
For more details on the API and datasets, visit https://research.stlouisfed.org/docs/api/fred/
The endpoint you will be most interested in is fred/series/observations, so you may want to read the docs for that one in particular.
You’ll need to create a FRED user account and API key for yourself, which you can do here: https://research.stlouisfed.org/useraccount/register/step1
Once you have an account, request your API key and use it in your requests.

##Requirements

1. Your application should fetch the following FRED series in their entirety:
• Real Gross Domestic Product (GDPC1)
• University of Michigan Customer Sentiment Index (UMCSENT)
• US Civilian Unemployment Rate (UNRATE)
2. Your application should store the observations in a relational database running on a localhost.
3. Your application should allow for two data flows: initial and incremental. The initial data flow should clear up the data persisted in the database (if any) and load it afresh. The incremental data flow should only load the data that is not present in the database yet.
4. Please answer the following question using the observations stored in your database:
What was the average rate of unemployment for each year starting in 1980 and going up to 2015?
About the application Application folder

config/config.py: config params models/models.py : database model utils/utils.py: others functions views/views.py: different views of the api runserver.py: main function of application tests.py: basic unit test
schema.sql : sql queries to create user, database, schema and tables
average_rate_of_unemployment_each_year.sql: average rate of unemployment for each year starting in 1980 and going up to 2015 SQL query
requirements.txt : python dependencies

##Application requirements

In order to build this project the following requirements must be met in the machine:
1. PostgreSQL
2. Python 2.7 or later
3. requirements.txt: pip install -r requirements.txt

##How to execute the application

In order to execute the application, the following command must be run in the root application folder:
 1. Execute schema.sql in order to create user, database, schema and tables that the application will use to persist the data.
2. python runserver.py : to run the application
  * Running on http://localhost:5000/ (Press CTRL+C to quit) * Restarting with stat
* Debugger is active!
* Debugger PIN: 312-265-684
http://0.0.0.0:80/incremental_load?series_id=<GDPC1 or UMCSENT or UNRATE >&other_parameters*

 ##Executing the data loads

Four services are available in the application under this URLs
http://0.0.0.0:80/initial_load?series_id=<GDPC1 or UMCSENT or UNRATE >&other_parameters*
   http://localhost:5000/check_data_loads http://localhost:5000/unemployment_rates
Only this URL are take in account in the application.
In order to load the data initially and incrementally, some endpoints were created to make it easy to perform such operations. They are described as follows.

#Initial load

http://0.0.0.0:80/initial_load?series_id=<GDPC1 or UMCSENT or UNRATE >&other_parameters*
Example : http://localhost:5000/initial_load?series_id=GDPC1
Example : http://localhost:5000/initial_load?series_id=GDPC1&limit=10
*other_parameters : all others parameters available except (api_key,file_type, series_id)on the native api (series_id, file_type, api_key ,limit, sort_order, observation_start, observation_end, output_type, vintage_dates)

#Incremental load

http://0.0.0.0:80/incremental_load?series_id=<GDPC1 or UMCSENT or UNRATE >&other_parameters*
Example : http://localhost:5000/incremental_load?series_id=GDPC1
Example : http://localhost:5000/incremental_load?series_id=GDPC1&limit=10

*other_parameters : all others parameters available except (api_key,file_type, series_id)on the native api (series_id, file_type, api_key ,limit, sort_order, observation_start, observation_end, output_type, vintage_dates)
At the end of each execution the resulting message is displayed:
 {
"timeSeries": "<series_id>",
 "message": "Inserted <Number of Observations> observations”
 }

##Verifying the data loads

In order verify the data load a endpoint was created. It return the 5 first rows of each tables.
http://localhost:5000/check_data_loads

  {
"Real_Gross_Domestic_Product": {
    "19470101": 1934.471,
    "19470401": 1932.281,
    "19470701": 1930.315,
    "19471001": 1960.705,
    "19480101": 1989.535
}, "US_Civilian_Unemployment_Rate": {
    "20151101": 5.0,
    "20151201": 5.0,
    "20160101": 4.9,
    "20160201": 4.9,
    "20160301": 5.0
}, "University_of_Michigan_Customer_Sentiment_Index": {
    "19521101": null,
    "19530201": null,
    "19530801": null,
    "19531101": null,
    "19540201": null
} }



##What was the average rate of unemployment for each year starting in 1980 and going up to 2015?

In order to answer this question the following SQL script was created:

SELECT
  extract(year from observation_date) AS year,
  AVG(unemployment_rate) avg_unemployment_rate
FROM FRED_SERIES.US_Civilian_Unemployment_Rate
WHERE extract(year from observation_date)  >= 1980 AND extract(year from observation_date) <= 2015
GROUP BY extract(year from observation_date)
ORDER BY extract(year from observation_date) DESC;


It can also be found in the file average_rate_of_unemployment_for_each_year.sql inside the project. It was also created an endpoint to see such results:
http://localhost:5000/unemployment_rates
The result of the above call is illustrated as follows:

{
  "1980": 7.175,
  "1981": 7.61666666666667,
  "1982": 9.70833333333333,
  "1983": 9.6,
  "1984": 7.50833333333333,
  "1985": 7.19166666666667,
  "1986": 7.0,
  "1987": 6.175,
  "1988": 5.49166666666667,
  "1989": 5.25833333333333,
  "1990": 5.61666666666667,
  "1991": 6.85,
  "1992": 7.49166666666667,
  "1993": 6.90833333333333,
  "1994": 6.1,
  "1995": 5.59166666666667,
  "1996": 5.40833333333333,
  "1997": 4.94166666666667,
  "1998": 4.5,
  "1999": 4.21666666666667,
  "2000": 3.96666666666667,
  "2001": 4.74166666666667,
  "2002": 5.78333333333333,
  "2003": 5.99166666666667,
  "2004": 5.54166666666667,
  "2005": 5.08333333333333,
  "2006": 4.60833333333333,
  "2007": 4.61666666666667,
  "2008": 5.8,
  "2009": 9.28333333333333,
  "2010": 9.60833333333333,
  "2011": 8.93333333333333,
  "2012": 8.075,
  "2013": 7.35833333333333,
  "2014": 6.175,
  "2015": 5.26666666666667
}


Test scenario

Few basic tests scenario was implemented too to check the availability of database tables, avec api services.
python tests.py
....... ---------------------------------------------------------------------- Ran 7 tests in 0.212s
OK
