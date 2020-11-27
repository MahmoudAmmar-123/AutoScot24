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
        self.available_make = []

        self.find_available_make()

    def find_available_make(self):
        """
        Finds all the avilable non-duplicate make in the 
        database listing.db

        The final list available_make will look like:
        [make_1, make_2, ...]
        """
        all_make = self.listing.get_all_make()
        all_make_list = [all_make[0] for all_make in all_make]

        for car in all_make_list:
            if car not in self.available_make:
                self.available_make.append(car)

        self.number_of_make = len(all_make_list)

    def percentile_distribution(self, make):
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
        make = self.listing.get_make_with_make(make)
        make_list = [make[0] for make in make]

        return int(len(make_list) / self.number_of_make * 100)

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
        for make in self.available_make:
            percentile_dict.update(
                {make: self.percentile_distribution(make)})

        # Arranging the result in descending order
        percentile_dict = dict(
            sorted(percentile_dict.items(), key=operator.itemgetter(1), reverse=True))

        return percentile_dict
