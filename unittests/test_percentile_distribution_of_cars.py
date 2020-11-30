import unittest
import os
import shutil

from database import ListingDataBase
from percentile_distribution_of_cars import PercentileDistributionOfCars


class TestPercentileDistributionOfCars(unittest.TestCase):
    def setUp(self):
        directory = './unittests/output'
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory)

        self.listing_db = ListingDataBase("./unittests/output/listings.db")
        self.listing_db.insert_csv_into_db("./unittests/input/listings.csv")

    def test_percentile_distribution(self):
        """
        Checks if the average is calculated correctly
        """
        percentile_distribution_of_cars = PercentileDistributionOfCars(self.listing_db)
        percentile = percentile_distribution_of_cars.percentile_distribution("Mazda")

        self.assertEqual(percentile, 30)

    def test_generate_dict_percentile_distribution(self):
        """
        Checks if the average is calculated correctly
        """
        percentile_distribution_of_cars = PercentileDistributionOfCars(self.listing_db)
        percentile = percentile_distribution_of_cars.generate_dict_percentile_distribution()

        self.assertEqual(percentile["Mazda"], 30)
        self.assertEqual(percentile["Audi"], 60)
        self.assertEqual(percentile["BWM"], 10)

def tearDown(self):
    directory = './unittests/output'
    shutil.rmtree(directory)
