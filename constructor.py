from database import ListingDataBase, ContactsDataBase
from operations import Operations

import os.path
import shutil


class Constructor:
    """
    Main class which runs all the operations
    """

    def __init__(self):
        directory = './output'
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory)

    def databases_constructor(self):
        """
        Operations for converting the csv input files into database
        """
        self.listing = ListingDataBase("./output/listings.db")
        self.listing.insert_csv_into_db("./input/listings.csv")

        self.contacts = ContactsDataBase("./output/contacts.db")
        self.contacts.insert_csv_into_db("./input/contacts.csv")

    def operations_constructor(self):
        """
        Operations for converting the csv input files into 
        """
        self.operations = Operations(self.listing, self.contacts)

        self.operations.average_listing_selling_price()
        self.operations.percentile_distribution()
        self.operations.average_price_thirty_percent()
        self.operations.top_five_contacted_listings_per_month()
        self.operations.output_operations_to_csv()


if __name__ == '__main__':
    main = Constructor()
    main.databases_constructor()
    main.operations_constructor()