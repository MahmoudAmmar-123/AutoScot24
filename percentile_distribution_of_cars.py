import operator


class PercentileDistributionOfCars:
    """
    Finds the percentile distribution of available cars by make

    Parameters
    ----------
    listing : databse
        the generated database for the listing information
        containing id, make, price, mileage and seller_type
    """

    def __init__(self, listing):
        self.listing = listing

    def percentile_distribution(self, make_name):
        """
        Calculates the percentile distribution of 
        a specified make

        Parameters
        ----------
        make : str
            the name of the manufacturer of the car

        Return
        ----------
        percentile : int
            the percentile of the specified make
        """
        make = self.listing.quer_component_using_column("make", "make", "Listings", make_name)
        make_list = [make[0] for make in make]
        total_number_of_make = self.listing.quer_number_of_rows_for_column("make", "Listings")

        return round((len(make_list) / total_number_of_make) * 100, 2)

    def generate_dict_percentile_distribution(self):
        """
        Parses the collected data into a dict

        Return
        ----------
        percentile_dict : dict
            the final result of all the percentile 
            distributions of available cars
        """
        percentile_dict = {}
        available_make = self.listing.quer_distinct_components("make", "Listings")
        for make in available_make:
            percentile_dict.update(
                {make: self.percentile_distribution(make)})

        # Arranging the result in descending order
        percentile_dict = dict(
            sorted(percentile_dict.items(), key=operator.itemgetter(1), reverse=True))

        return percentile_dict
