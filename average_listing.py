

class AverageListing:
    """
    Finds the average listing selling price per 
    seller type using the database listing.db

    Parameters
    ----------
    listing : databse
        the generated database for the listing information
        containing id, make, price, mileage and seller_type
    """

    def __init__(self, listing):
        self.listing = listing

    def find_avg_price(self, seller_type):
        """
        Calculates the average price for a specified seller_type

        Parameters
        ----------
        seller_type : str
            either dealer, private or other

        Return
        ----------
        average_price : int
            calculated average price for each seller_type
        """
        price = self.listing.quer_component_using_column("price", "seller_type", "Listings", seller_type)
        price_list = [price[0] for price in price]
        average_price = int(sum(price_list)/len(price_list))

        return average_price

    def generate_dict_avg_listing(self):
        """
        Parses the collected data into a dict

        Return
        ----------
        avg_listing : dict
            contains the final result for all the seller_type
        """
        avg_listing = {
            'dealer': self.find_avg_price('dealer'),
            'private': self.find_avg_price('private'),
            'other': self.find_avg_price('other')
        }

        return avg_listing
