import operator


class AveragePriceThirtyPercent:
    """
    Finds the average price of the 30% most contacted
    listings using the databases contacts.db and listing.db

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

        self.available_listing_ids = []
        self.price_list = []
        self.listing_id_count = {}

        self.find_available_listing_ids()
        self.find_top_thirty_percent()

    def find_available_listing_ids(self):
        """
        Finds all the available non-deuplicate listing_id
        from the database contacts.db

        The final list all_contacts_table will look like:
        [listing_id_1, listing_id_2, ...]
        """
        # Get all listing_id from the contacts database then put them in a list
        all_listing_ids = self.contacts.get_all_listing_ids()
        all_listing_ids_list = [all_listing_ids[0]
                                for all_listing_ids in all_listing_ids]

        # Checks if there is a duplicate for each listing_id then appends it if not
        for list_id in all_listing_ids_list:
            if list_id not in self.available_listing_ids:
                self.available_listing_ids.append(list_id)

    def find_top_thirty_percent(self):
        """
        First, it creates a list listing_id_count with the 
        number of contact for each listing_id. Second, it 
        finds the top 30% of the listing_id_count

        The final list listing_id_count will look like:
        {
            listing_id_1 : number_of_times_contacted_1,
            listing_id_2 : number_of_times_contacted_2, ...
        }
        """
        for listing in self.available_listing_ids:
            listing_id = self.contacts.get_listing_id_with_listing(listing)
            self.listing_id_count.update({listing: len(listing_id)})

        # Arranging listing_id_count in descending order the selecting
        # the top 30% from the list
        number_of_top_thirty_persent = int(len(self.listing_id_count) * 0.30)
        self.listing_id_count = dict(sorted(self.listing_id_count.items(
        ), key=operator.itemgetter(1), reverse=True)[:number_of_top_thirty_persent])

    def find_prices_of_top_thirty_percent(self):
        """
        First, it gets the price of each one of the top 30% most 
        contacted listings from the database listing.db. Second, 
        it calculated the average price

        Returns
        ----------
        average_price : int
            The average price of the calculated top 30%
        """
        for listing_id, count in self.listing_id_count.items():
            price_with_id = self.listing.get_price_with_id(listing_id)
            self.price_list.append(price_with_id[0][0])

        return int(sum(self.price_list) / len(self.price_list))
