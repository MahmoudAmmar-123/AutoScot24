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

        self.top_five_listing_ids_per_month = {}

        self.find_top_five_most_contacted_listings_per_month()
        
    def find_top_five_most_contacted_listings_per_month(self):
        """
        First, it finds the total amount of contacts for each 
        listing_id. Second, it finds the top most contacted 
        listings. 

        The dict top_five_listing_ids_per_month will look like:
        {
            readable_date_1 : [
                [total_amount_of_contacts_1, listing_id_1],
                [total_amount_of_contacts_2, listing_id_2], ...
            ],
            readable_date_2 : [
                [total_amount_of_contacts_1, listing_id_1],
                [total_amount_of_contacts_2, listing_id_2], ...
            ], ...
        }
        """
        available_dates = self.contacts.quer_distinct_components("contact_date", "Contacts")
        available_listing_ids = self.contacts.quer_distinct_components("listing_id", "Contacts")
        
        self.ordered = {}
        for date in available_dates:
            listing = []
            month = self.contacts.quer_component_using_column("listing_id", "contact_date", "Contacts", date)
            new = [month[0] for month in month]
            for listing_id in available_listing_ids:
                count = new.count(listing_id)
                listing.append([count, listing_id])
                listing = sorted(listing, key=lambda x: x[0], reverse=True)

            self.ordered[date] = listing[:5]
            
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
        available_dates = self.contacts.quer_distinct_components("contact_date", "Contacts")
        for date in available_dates:
            top_five = self.ordered[date]
            all_months[date] = {}

            # Loops over top five to append their components to the final dict
            for index in range(len(top_five)):
                listing_id = top_five[index][1]
                total_contacts = top_five[index][0]

                all_months[date].update(
                    {
                        index+1: {
                            'Ranking': index+1,
                            'Listing Id': listing_id,
                            'Make': self.listing.quer_component_using_column("make", "id", "Listings", listing_id)[0][0],
                            'Selling Price': self.listing.quer_component_using_column("price", "id", "Listings", listing_id)[0][0],
                            'Mileage': self.listing.quer_component_using_column("mileage", "id", "Listings", listing_id)[0][0],
                            'Total Amount of Contacts': total_contacts
                        }
                    }
                )

        return all_months

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
        all_contacts_table = TopFiveContactedListingsPerMonth.adjust_unix_timestamp(
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
