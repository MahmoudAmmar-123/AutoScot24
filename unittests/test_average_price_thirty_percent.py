import unittest
import os
import shutil

from database import ListingDataBase, ContactsDataBase
from average_price_thirty_percent import AveragePriceThirtyPercent


class TestAveragePriceThirtyPercent(unittest.TestCase):
    def setUp(self):
        directory = './unittests/output'
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory)

        self.listing_db = ListingDataBase("./unittests/output/listings.db")
        self.listing_db.insert_csv_into_db("./unittests/input/listings.csv")

        self.contacts_db = ContactsDataBase("./unittests/output/contacts.db")
        self.contacts_db.insert_csv_into_db("./unittests/input/contacts.csv")

    def test_find_top_percentile(self):
        """
        Checks if the average is calculated correctly
        """
        average_price_thirty_percent = AveragePriceThirtyPercent(self.contacts_db, self.listing_db)
        top_percentile = average_price_thirty_percent.find_top_percentile(30/100)

        self.assertEqual(top_percentile[0], [1276, 14])
        self.assertEqual(top_percentile[1], [1038, 6])
        self.assertEqual(top_percentile[2], [1288, 1])
        self.assertEqual(top_percentile[3], [1263, 1])
        self.assertEqual(top_percentile[4], [1257, 1]) 
        self.assertEqual(top_percentile[5], [1244, 1])

def tearDown(self):
    directory = './unittests/output'
    shutil.rmtree(directory)
