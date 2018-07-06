from runserver import app, db
from models.models import US_Civilian_Unemployment_Rate,University_of_Michigan_Customer_Sentiment_Index,Real_Gross_Domestic_Product
import unittest

class BasicTestCase(unittest.TestCase):

    def testIndex(self):
        """initial test. ensure flask was set up correctly"""
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def testGetInitialLoad(self):
        """Initial Load  rates """
        response = app.test_client(self).get('/initial_load')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)

    def testGetIncrementalLoad(self):
        """Initial Load  rates """
        response = app.test_client(self).get('/incremental_load')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)

    def testGetUnemploymentRates(self):
        """Test Unemployment rates """
        response = app.test_client(self).get('/unemployment_rates')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_US_Civilian_Unemployment_Rate(self):
        ucur = US_Civilian_Unemployment_Rate('1900-01-01', 0.001)
        db.session.add(ucur)
        db.session.commit()

    def test_University_of_Michigan_Customer_Sentiment_Index(self):
        umcsi = University_of_Michigan_Customer_Sentiment_Index('1900-01-01', 0.001)
        db.session.add(umcsi)
        db.session.commit()


    def test_Real_Gross_Domestic_Product(self):
        rgdp = Real_Gross_Domestic_Product('1900-01-01', 0.001)
        db.session.add(rgdp)
        db.session.commit()

if __name__ == '__main__':
    unittest.main()