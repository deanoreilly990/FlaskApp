import unittest
import App.models as models
import App.DataHistory as DH


# Unit test class - used to ensure that the application is able to access the various resources it needs.
class test_connection_exist(unittest.TestCase):
    def test_Daft(self): #Test connection Status to the Database Daft
       self.assertTrue(models.test_databaseDaft())
    def test_Hist(self): # Test Connection status to Databse Hist
       self.assertTrue(models.test_databaseHist())
    def test_imagePath(self): # Check Paths are accessable
        self.assertTrue(DH.testpath('App/static/images'))
        self.assertTrue(DH.testpath('App/static/images/2017'))
        self.assertTrue(DH.testpath('App/static/images/history'))
        self.assertTrue(DH.testpath('App/static/images/History'))

def main():
    unittest.main()
