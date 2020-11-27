from datetime import datetime
from itertools import islice

import operator


class TopFiveContactedListingsPerMonth:
    """
    Finds the top five most contacted listing for each
    month using the databases contacts.db and listing.db

    Parameters
    ----------
    contacts : database
        the generated database for the contacts information
        containing listing_id and contact_date
    listing : databse
        the generated database for the listing information
        containing id, make, price, mileage and seller_type
    """

    def __init__(self, contacts, listing):
        self.contacts = contacts
        self.listing = listing

        self.available_contact_dates = []
        self.top_five_listing_ids_per_month = {}

        self.convert_contact_date_to_readable_format()
        self.find_available_dates()
        self.find_top_five_most_contacted_listings_per_month()

    def convert_contact_date_to_readable_format(self):
        """
        Converts the unix timestamp to readable date, and gets a 
        list that contains the readable_dates with its listing_id

        The final list all_contacts_table will look like:
        [
            [listing_id_1, readable_date_1],
            [listing_id_2, readable_date_2], ...
        ]
        """
        # Get contact_dates from the contacts database then puts them in a list
        all_contact_dates = self.contacts.get_all_contact_dates()
        self.all_contacts_table = [[all_contact_dates[0], all_contact_dates[1]]
                                   for all_contact_dates in all_contact_dates]

        # all_contacts_table with proper unix timestamp digit numbers
        self.all_contacts_table = TopFiveContactedListingsPerMonth.adjust_unix_timestamp(
            self.all_contacts_table)

        # all_contacts_table with readable timestamp
        for index in range(len(self.all_contacts_table)):
            self.all_contacts_table[index][1] = datetime.utcfromtimestamp(
                self.all_contacts_table[index][1]).strftime('%Y-%m')

    def find_available_dates(self):
        """
        Finds the contact_dates in the database without duplicates

        The list available_contact_dates will look like:
        [readable_date_1, readable_date_2, ...]
        """
        for contacts_row in self.all_contacts_table:
            if contacts_row[1] not in self.available_contact_dates:
                self.available_contact_dates.append(contacts_row[1])

    def find_top_five_most_contacted_listings_per_month(self):
        """
        First, it finds the total amount of contacts for each 
        listing_id. Second, it finds the top most contacted 
        listings. 

        The dict top_five_listing_ids_per_month will look like:
        {
            readable_date_1 : [
                (listing_id_1, total_amount_of_contacts_1),
                (listing_id_2, total_amount_of_contacts_2), ...
            ],
            readable_date_2 : [
                (listing_id_1, total_amount_of_contacts_1),
                (listing_id_2, total_amount_of_contacts_2), ...
            ], ...
        }
        """
        contacts_for_one_month = []
        for date in self.available_contact_dates:
            for contacts_table in self.all_contacts_table:
                # Collects all listing_id with the same date in one list
                if contacts_table[1] == date:
                    contacts_for_one_month.append(contacts_table[0])

            # Finds the total amount of contacts in contacts_for_one_month for each listing_id
            listing_id_count = {i: contacts_for_one_month.count(
                i) for i in contacts_for_one_month}

            # Sort listing_id_count in descending order
            listing_id_count_descending = dict(
                sorted(listing_id_count.items(), key=operator.itemgetter(1), reverse=True))

            # Select the top five most contacted listings from the listing_id_count_descending dict
            self.top_five_listing_ids_per_month.update(
                {date: list(islice(listing_id_count_descending.items(), 5))})

    def generate_dict_top_five(self):
        """
        Parses the collected data into a dict

        The dict all_months will look like:
        {
            readable_date_1 : {
                index_1 : {
                    'Ranking' : ranking_value,
                    'Listing Id' : listing_id_value,
                    'Make' : make_name,
                    'Selling Price' : price_value,
                    'Mileage' : mileage_value,
                    'Total Amount of Contacts' : total_contacts_value
                }, ...
            }, ...
        }
        """
        all_months = {}
        # Loops over each avilable non-duplicate date
        for date in self.available_contact_dates:
            top_five = self.top_five_listing_ids_per_month[date]
            all_months[date] = {}

            # Loops over top five to append their components to the final dict
            for index in range(len(top_five)):
                listing_id = top_five[index][0]
                total_contacts = top_five[index][1]

                all_months[date].update(
                    {
                        index+1: {
                            'Ranking': index+1,
                            'Listing Id': listing_id,
                            'Make': self.listing.get_make_with_id(listing_id)[0][0],
                            'Selling Price': self.listing.get_price_with_id(listing_id)[0][0],
                            'Mileage': self.listing.get_mileage_with_id(listing_id)[0][0],
                            'Total Amount of Contacts': total_contacts
                        }
                    }
                )

        return all_months

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
                all_contact_dates_list[index][1] = int(
                    all_contact_dates_list[index][1] / number_to_divide_with)

        return all_contact_dates_list
