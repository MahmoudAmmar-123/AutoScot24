import csv
import sqlite3


class ListingDataBase:
    """
    The database for listing.csv
    """

    def __init__(self):
        self.conn = sqlite3.connect("./output/listings.db")
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE Listings (id INT, make STRING, price REAL, mileage REAL, seller_type STRING);")

    def execute(self, query, data):
        self.cur.execute(query, data)
        self.conn.commit()

    def create_listing_db(self):
        """
        Reads the csv file then inserts the data into the listing.db file
        """
        with open('./input/listings.csv', 'r') as fin:
            dr = csv.DictReader(fin)
            to_db = [(i['id'], i['make'], i['price'],
                      i['mileage'], i['seller_type']) for i in dr]

        self.cur.executemany(
            "INSERT INTO Listings (id, make, price, mileage, seller_type) VALUES (?, ?, ?, ?, ?);", to_db)
        self.conn.commit()

    def get_price_with_seller_type(self, seller_type):
        """
        Finds in the databse all the prices for a specific seller_type

        Parameters
        ----------
        seller_type : str
            either dealer, private or other
        """
        self.execute(
            "SELECT price FROM Listings WHERE seller_type = ?;", (seller_type,))
        return self.cur.fetchall()

    def get_price_with_id(self, listing_id):
        """
        Finds in the databse all the prices for a specific listing_id

        Parameters
        ----------
        listing_id : int
            the number of the listing
        """
        self.execute(
            "SELECT price FROM Listings WHERE id = ?;", (listing_id,))
        return self.cur.fetchall()

    def get_make_with_id(self, listing_id):
        """
        Finds in the databse all the make for a specific listing_id

        Parameters
        ----------
        listing_id : int
            the number of the listing
        """
        self.execute(
            "SELECT make FROM Listings WHERE id = ?;", (listing_id,))
        return self.cur.fetchall()

    def get_mileage_with_id(self, listing_id):
        """
        Finds in the databse all the mileage for a specific listing_id

        Parameters
        ----------
        listing_id : int
            the number of the listing
        """
        self.execute(
            "SELECT mileage FROM Listings WHERE id = ?;", (listing_id,))
        return self.cur.fetchall()

    def get_all_make(self):
        """
        Finds in the databse all the make
        """
        self.cur.execute("SELECT make FROM Listings")
        return self.cur.fetchall()

    def get_make_with_make(self, make):
        """
        Finds in the databse all the make for a specific make

        Parameters
        ----------
        make : str
            the name of the manufacturer company
        """
        self.execute(
            "SELECT make FROM Listings WHERE make = ?;", (make,))
        return self.cur.fetchall()

    def __del__(self):
        """
        Destroys instance and connection on completion of called method 
        """
        self.conn.close()
