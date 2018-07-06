from runserver import db, app

#Real Gross Domestic Product
class Real_Gross_Domestic_Product(db.Model):

  __tablename__ = app.config.get('DATABASE_SCHEMA')+".Real_Gross_Domestic_Product"
  __table_args__ = {'quote': False}
  observation_date = db.Column(db.Date, primary_key=True)
  rgdp_value = db.Column(db.Float)

  def __init__(self, observation_date, rgdp_value):
    self.observation_date = observation_date
    self.rgdp_value = rgdp_value

  def __repr__(self):
    return "<observation_date {}, rgdp_value {}>".format(self.observation_date, self.rgdp_value)



#University of Michigan Customer Sentiment Index
class University_of_Michigan_Customer_Sentiment_Index (db.Model):

  __tablename__ = app.config.get('DATABASE_SCHEMA')+".University_of_Michigan_Customer_Sentiment_Index"
  __table_args__ = {'quote': False}
  observation_date = db.Column(db.Date, primary_key=True)
  sentiment_index = db.Column(db.Float)

  def __init__(self, observation_date, sentiment_index):
    self.observation_date = observation_date
    self.sentiment_index = sentiment_index

  def __repr__(self):
    return "<observation_date {}, sentiment_index {}>".format(self.observation_date, self.sentiment_index)




#US Civilian Unemployment Rate
class US_Civilian_Unemployment_Rate(db.Model):

  __tablename__ = app.config.get('DATABASE_SCHEMA')+".US_Civilian_Unemployment_Rate"
  __table_args__ = {'quote': False}
  observation_date = db.Column(db.Date, primary_key=True)
  unemployment_rate = db.Column(db.Float)

  def __init__(self, observation_date, unemployment_rate):
    self.observation_date = observation_date
    self.unemployment_rate = unemployment_rate

  def __repr__(self):
    return "<observation_date {}, unemployment_rate {}>".format(self.observation_date, self.unemployment_rate)
