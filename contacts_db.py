import csv
import sqlite3


class ContactsDataBase:
    """
    The database for contacts.csv
    """

    def __init__(self):
        self.conn = sqlite3.connect("./output/contacts.db")
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE Contacts (listing_id INT, contact_date INT);")

    def execute(self, query, data):
        self.cur.execute(query, data)
        self.conn.commit()

    def create_contacts_db(self):
        """
        Reads the csv file then inserts the data into the contacts.db file
        """
        with open('./input/contacts.csv', 'r') as fin:
            dr = csv.DictReader(fin)
            to_db = [(i['listing_id'], i['contact_date']) for i in dr]

        self.cur.executemany(
            "INSERT INTO Contacts (listing_id, contact_date) VALUES (?, ?);", to_db)
        self.conn.commit()

    def get_all_listing_ids(self):
        """
        Finds in the databse all the listing_id
        """
        self.cur.execute("SELECT listing_id FROM Contacts")
        return self.cur.fetchall()

    def get_all_contact_dates(self):
        """
        Finds in the databse all the elements
        """
        self.cur.execute("SELECT * FROM Contacts")
        return self.cur.fetchall()

    def get_listing_id_with_listing(self, listing):
        """
        Finds in the databse all the listing_id for a specific listing_id

        Parameters
        ----------
        listing : int
            the number of the listing
        """
        self.execute(
            "SELECT listing_id FROM Contacts WHERE listing_id = ?;", (listing,))
        return self.cur.fetchall()

    def __del__(self):
        """
        Destroys instance and connection on completion of called method 
        """
        self.conn.close()
