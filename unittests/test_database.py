import unittest
import os
import shutil

from database import ListingDataBase, ContactsDataBase


class TestDataBase(unittest.TestCase):
    def setUp(self):
        directory = './unittests/output'
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory)

        self.listing_db = ListingDataBase("./unittests/output/listings.db")
        self.listing_db.insert_csv_into_db("./unittests/input/listings.csv")

        self.contacts_db = ContactsDataBase("./unittests/output/contacts.db")
        self.contacts_db.insert_csv_into_db("./unittests/input/contacts.csv")

    def test_insert_csv_into_db_listings_db_and_quer_column(self):
        """
        Checks if first three rows in the database are correct
        """
        all_column_make = self.listing_db.quer_column("make", "Listings")
        all_column_list_make = [all_column_make[0] for all_column_make in all_column_make]

        self.assertEqual(all_column_list_make[0], "Audi")
        self.assertEqual(all_column_list_make[1], "Mazda")
        self.assertEqual(all_column_list_make[2], "BWM")

        all_column_price = self.listing_db.quer_column("price", "Listings")
        all_column_list_price = [all_column_price[0] for all_column_price in all_column_price]

        self.assertEqual(all_column_list_price[0], 49717.0)
        self.assertEqual(all_column_list_price[1], 22031.0)
        self.assertEqual(all_column_list_price[2], 17742.0)

        all_column_mileage = self.listing_db.quer_column("mileage", "Listings")
        all_column_list_mileage= [all_column_mileage[0] for all_column_mileage in all_column_mileage]

        self.assertEqual(all_column_list_mileage[0], 6500.0)
        self.assertEqual(all_column_list_mileage[1], 7000.0)
        self.assertEqual(all_column_list_mileage[2], 6000.0)

        all_column_seller_type = self.listing_db.quer_column("seller_type", "Listings")
        all_column_list_seller_type = [all_column_seller_type[0] for all_column_seller_type in all_column_seller_type]

        self.assertEqual(all_column_list_seller_type[0], 'private')
        self.assertEqual(all_column_list_seller_type[1], 'private')
        self.assertEqual(all_column_list_seller_type[2], 'dealer')

    def test_insert_csv_into_db_contacts_db_and_quer_column(self):
        """
        Checks if first three rows in the database are correct
        """
        all_column_make = self.contacts_db.quer_column("listing_id", "Contacts")
        all_column_list_make = [all_column_make[0] for all_column_make in all_column_make]

        self.assertEqual(all_column_list_make[0], 1244)
        self.assertEqual(all_column_list_make[1], 1085)
        self.assertEqual(all_column_list_make[2], 1288)

        all_column_make = self.contacts_db.quer_column("contact_date", "Contacts")
        all_column_list_make = [all_column_make[0] for all_column_make in all_column_make]

        self.assertEqual(all_column_list_make[0], "2020-06")
        self.assertEqual(all_column_list_make[1], "2020-02")
        self.assertEqual(all_column_list_make[2], "2020-01")

    def test_quer_component_using_column(self):
        """
        Checks if the components of a column based on 
        another components of a columns is correct
        """
        all_column = self.listing_db.quer_component_using_column("make", "seller_type", "Listings", "other")
        all_column_list = [all_column[0] for all_column in all_column]

        self.assertEqual(all_column_list[0], "Mazda")
        self.assertEqual(all_column_list[1], "Mazda")

    def test_quer_distinct_components(self):
        """
        Checks if the selected components of a column 
        includes all distinct components
        """
        distinct_components = self.listing_db.quer_distinct_components("make", "Listings")

        self.assertEqual(distinct_components[0], "Audi")
        self.assertEqual(distinct_components[1], "Mazda")
        self.assertEqual(distinct_components[2], "BWM")

    def test_quer_number_of_rows_for_column(self):
        """
        Checks if the quered total number of rows 
        for a specified column is correct
        """
        total_number_of_rows = self.listing_db.quer_number_of_rows_for_column("make", "Listings")

        self.assertEqual(total_number_of_rows, 10)

    def test_quer_list_of_duplicates(self):
        """
        Checks if the quered number of duplicates is correct
        """
        duplicates = self.listing_db.quer_list_of_duplicates("make", "Listings")

        self.assertEqual(duplicates[0], ['Audi', 6])
        self.assertEqual(duplicates[1], ['Mazda', 3])
        self.assertEqual(duplicates[2], ['BWM', 1])

def tearDown(self):
    directory = './unittests/output'
    shutil.rmtree(directory)
