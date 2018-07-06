
class BaseConfig:

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USER_NAME = "fred_user"
    USER_PASSWORD = "fred_password"
    DATABASE_NAME = "fred"
    SQLALCHEMY_DATABASE_URI = 'postgresql://'+USER_NAME+':'+USER_PASSWORD+'@0.0.0.0/'+DATABASE_NAME+''
    API_URL = "https://api.stlouisfed.org/fred/series/observations"
    API_KEY = "872f4dd75d152a111b2485a0faef3daf"
    DATABASE_SCHEMA = "series"
