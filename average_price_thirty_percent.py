import operator


class AveragePriceThirtyPercent:
    """
    Finds the average price of the percentile of most contacted
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

        self.price_list = []

    def find_average_of_top_percentile(self, percentage):
        """
        First, it gets the price of each one of the top percentile most 
        contacted listings from the database listing.db. Second, 
        it calculats the average price

        Returns
        ----------
        average_price : int
            The average price of the calculated top percentile
        """
        top_percentile = self.find_top_percentile(percentage)
        for row in top_percentile:
            price_with_id = self.listing.quer_component_using_column("price", "id", "Listings", row[0])
            self.price_list.append(price_with_id[0][0])

        return int(sum(self.price_list) / len(self.price_list))

    def find_top_percentile(self, percentage):
        """
        First, it creates a list list_of_duplicates with the 
        number of contact for each listing_id. Second, it 
        finds the top percentile of the list_of_duplicates

        The final list list_of_duplicates will look like:
        [
            [available_component_1, number_of_duplication_1],
            [available_component_2, number_of_duplication_2], ...
        ]

        Parameters
        ----------
        pecentage : float
            the percentile used to find the specifications
        """
        list_of_duplicates = self.contacts.quer_list_of_duplicates("listing_id", "Contacts")
        number_of_top_percentile = int(len(list_of_duplicates) * 0.30)
        
        return list_of_duplicates[:number_of_top_percentile]
