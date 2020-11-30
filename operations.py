from average_listing import AverageListing
from percentile_distribution_of_cars import PercentileDistributionOfCars
from average_price_thirty_percent import AveragePriceThirtyPercent
from top_five_contacted_listings_per_month import TopFiveContactedListingsPerMonth
from output_to_csv import OutputToCSV
from datetime import datetime


class Operations:

    def __init__(self, listings, contacts):
        self.listings = listings
        self.contacts = contacts

    def average_listing_selling_price(self):
        """
        Finds the average listing selling price per seller type
        """
        operations = AverageListing(self.listings)
        self.avg_listing = operations.generate_dict_avg_listing()

    def percentile_distribution(self):
        """
        Finds the percentile distribution of available cars by make
        """
        self.percentile_distribution_of_cars = PercentileDistributionOfCars(
            self.listings)
        self.percentile = self.percentile_distribution_of_cars.generate_dict_percentile_distribution()

    def average_price_thirty_percent(self):
        """
        Finds th average price of the 30% most contacted listings
        """
        self.average_price = AveragePriceThirtyPercent(
            self.contacts, self.listings)
        self.thirty_percent = self.average_price.find_average_of_top_percentile(30/100)

    def top_five_contacted_listings_per_month(self):
        """
        Finds the top 5 most contacted listings per month
        """
        self.top_five = TopFiveContactedListingsPerMonth(
            self.contacts, self.listings)
        self.top_five_most_contacted = self.top_five.generate_dict_top_five()

    def output_operations_to_csv(self):
        """
        Outpurs all the above operations into separate csv files
        """
        self.output_to_csv = OutputToCSV(
            self.avg_listing, self.percentile, self.thirty_percent, self.top_five_most_contacted)
        self.output_to_csv.write_avg_price()
        self.output_to_csv.write_percentile()
        self.output_to_csv.write_avg_price_top_thirty_percent()
        self.output_to_csv.write_top_five_most_contacted()

    @staticmethod
    def convert_contact_date_to_readable_format(csv_data):
        """
        Converts the unix timestamp to readable date, and gets a 
        list that contains the readable_dates with its listing_id

        The final list all_contacts_table will look like:
        [
            [listing_id_1, readable_date_1],
            [listing_id_2, readable_date_2], ...
        ]
        """
        # all_contacts_table with proper unix timestamp digit numbers
        csv_data = [[csv_data[0], csv_data[1]] for csv_data in csv_data]
        all_contacts_table = Operations.adjust_unix_timestamp(
            csv_data)

        # all_contacts_table with readable timestamp
        for index in range(len(all_contacts_table)):
            all_contacts_table[index][1] = datetime.utcfromtimestamp(
                all_contacts_table[index][1]).strftime('%Y-%m')

        return all_contacts_table

    @staticmethod
    def adjust_unix_timestamp(all_contact_dates_list):
        """
        Brings each timestamp in the contact_date 
        back to unix timestamps range

        Parameters
        ----------
        all_contact_dates_list : list
            contains listing_id and contact_date 
            in unix timestamp

        Return
        ----------
        all_contact_dates_list : list
            contains listing_id and contact_date 
            in readable format
        """
        for index in range(len(all_contact_dates_list)):
            digits_in_unix_timestamp = 10
            number_to_divide_with = '1'
            date = len(str(all_contact_dates_list[index][1]))
            if int(date) > digits_in_unix_timestamp:
                zeros_to_remove = date-digits_in_unix_timestamp
                number_to_divide_with = int(
                    number_to_divide_with.ljust(zeros_to_remove+1, '0'))
                all_contact_dates_list[index][1] = int(int(all_contact_dates_list[index][1]) / number_to_divide_with)

        return all_contact_dates_list
