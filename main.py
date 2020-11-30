from database import ListingDataBase, ContactsDataBase
from average_listing import AverageListing
from percentile_distribution_of_cars import PercentileDistributionOfCars
from average_price_thirty_percent import AveragePriceThirtyPercent
from top_five_contacted_listings_per_month import TopFiveContactedListingsPerMonth
from output_to_csv import OutputToCSV

import os.path
import shutil


class Main:
    """
    Main class which runs all the operations
    """

    def __init__(self):
        directory = './output'
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory)

    def csv_to_db(self):
        """
        Operations for converting the csv input files into database
        """
        self.listing = ListingDataBase("./output/listings.db")
        self.listing.insert_csv_into_db("./input/listings.csv")
        self.contacts = ContactsDataBase("./output/contacts.db")
        self.contacts.insert_csv_into_db("./input/contacts.csv")

    def average_listing_selling_price(self):
        """
        Finds the average listing selling price per seller type
        """
        operations = AverageListing(self.listing)
        self.avg_listing = operations.generate_dict_avg_listing()

    def percentile_distribution(self):
        """
        Finds the percentile distribution of available cars by make
        """
        percentile_distribution_of_cars = PercentileDistributionOfCars(
            self.listing)
        self.percentile = percentile_distribution_of_cars.generate_dict_percentile_distribution()

    def average_price_thirty_percent(self):
        """
        Finds th average price of the 30% most contacted listinggs
        """
        average_price_thirty_percent = AveragePriceThirtyPercent(
            self.contacts, self.listing)
        self.thirty_percent = average_price_thirty_percent.find_average_of_top_percentile(30/100)

    def top_five_contacted_listings_per_month(self):
        """
        Finds the top 5 most contacted listings per month
        """
        top_five = TopFiveContactedListingsPerMonth(
            self.contacts, self.listing)
        self.top_five_most_contacted = top_five.generate_dict_top_five()

    def output_operations_to_csv(self):
        """
        Outpurs all the above operations into separate csv files
        """
        output_to_csv = OutputToCSV(
            self.avg_listing, self.percentile, self.thirty_percent, self.top_five_most_contacted)
        output_to_csv.write_avg_price()
        output_to_csv.write_percentile()
        output_to_csv.write_avg_price_top_thirty_percent()
        output_to_csv.write_top_five_most_contacted()


if __name__ == '__main__':
    main = Main()
    main.csv_to_db()
    main.average_listing_selling_price()
    main.percentile_distribution()
    main.average_price_thirty_percent()
    main.top_five_contacted_listings_per_month()
    main.output_operations_to_csv()
