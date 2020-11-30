import unittest
import os
import shutil

from database import ListingDataBase
from average_listing import AverageListing


class TestAverageListing(unittest.TestCase):
    def setUp(self):
        directory = './unittests/output'
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory)

        self.listing_db = ListingDataBase("./unittests/output/listings.db")
        self.listing_db.insert_csv_into_db("./unittests/input/listings.csv")

    def test_find_avg_price(self):
        """
        Checks if the average is calculated correctly
        """
        average_listing = AverageListing(self.listing_db)
        average = average_listing.find_avg_price("other")

        self.assertEqual(average, 31472)

    def test_generate_dict_avg_listing(self):
        """
        Checks if average calculated in dict is correct
        """
        average_listing = AverageListing(self.listing_db)
        avg_listing_dict = average_listing.generate_dict_avg_listing()

        self.assertEqual(avg_listing_dict["dealer"], 22102)
        self.assertEqual(avg_listing_dict["private"], 38471)
        self.assertEqual(avg_listing_dict["other"], 31472)

def tearDown(self):
    directory = './unittests/output'
    shutil.rmtree(directory)
