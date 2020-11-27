import csv


class OutputToCSV:
    """
    Outputs all the operation results into a separate csv file

    Parameters
    ----------
    avg_listing : dict
    percentile : databse
    thirty_percent : int
    top_five_most_contacted : dict
    """

    def __init__(self, avg_listing, percentile, thirty_percent, top_five_most_contacted):
        self.avg_listing = avg_listing
        self.percentile = percentile
        self.thirty_percent = thirty_percent
        self.top_five_most_contacted = top_five_most_contacted

    def write_avg_price(self):
        with open('./output/avg_listing_selling_per_seller_type.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Seller Type", "Average in Euro"])
            writer.writerow(
                ['private', "€ " + str(self.avg_listing['private']) + ",-"])
            writer.writerow(
                ['dealer', "€ " + str(self.avg_listing['dealer']) + ",-"])
            writer.writerow(
                ['other', "€ " + str(self.avg_listing['other']) + ",-"])

    def write_percentile(self):
        with open('./output/percentile_distribution_of_cars.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Make", "Distribution"])
            for make, percentile in self.percentile.items():
                writer.writerow([make, str(percentile) + "%"])

    def write_avg_price_top_thirty_percent(self):
        with open('./output/avg_price_top_thirty_percent_most_contacted.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Average Price"])
            writer.writerow(["€ " + str(self.thirty_percent) + ",-"])

    def write_top_five_most_contacted(self):
        with open('./output/top_five_most_contacted.csv', 'w', newline='') as file:
            writer = csv.writer(file)

            for date, index in self.top_five_most_contacted.items():
                writer.writerow(["Month: " + date])
                writer.writerow(["Ranking", "Listing id", "Make",
                                 "Selling Price", "Mileage", "Total Amount of Contacts"])
                for elements in index:
                    writer.writerow([
                        index[elements]["Ranking"],
                        index[elements]["Listing Id"],
                        index[elements]["Make"],
                        "€ " + str(index[elements]["Selling Price"]) + ",-",
                        str(index[elements]["Mileage"]) + " KM",
                        index[elements]["Total Amount of Contacts"],
                    ])
                writer.writerow([""])
