import csv
import sqlite3

from operations import Operations


class DataBase:
    """
    The database for listing.csv
    """

    def __init__(self, output_directory):
        self.conn = sqlite3.connect(output_directory)
        self.cur = self.conn.cursor()

    def quer_column(self, column, database):
        """
        Finds in the databse all the make
        """
        self.cur.execute("SELECT " + column + " FROM " + database)
        self.conn.commit()
        return self.cur.fetchall()

    def quer_component_using_column(self, column1, column2, database, component):
        """
        Finds in the databse the components of column1 using specified component of column2

        Parameters
        ----------
        make : str
            the name of the manufacturer company
        """
        self.cur.execute("SELECT " + column1 + " FROM " + database + " WHERE " + column2 + " = ?;", (component,))
        self.conn.commit()
        return self.cur.fetchall()

    def quer_distinct_components(self, column, database):
        """
        Finds in the databse all the components of a 
        column without duplications

        Parameters
        ----------
        make : str
            the name of the manufacturer company

        Returns
        -------
        distinct_components : list
            A list with all the available components
            in a column without duplicates
        """
        self.cur.execute("SELECT DISTINCT " + column + " FROM " + database)
        distinct_components = self.cur.fetchall()
        return [distinct_components[0] for distinct_components in distinct_components]

    def quer_number_of_rows_for_column(self, column, database):
        """
        Finds the total number of rows for a specified column

        Parameters
        ----------
        column : str
            the name of the manufacturer company
        database : str
            the name of the manufacturer company

        Returns
        -------
        number_of_rows : int
        """
        self.cur.execute("SELECT COUNT ( " + column + " ) FROM " + database)
        number = self.cur.fetchall()
        return number[0][0]

    def quer_list_of_duplicates(self, column, database):
        """
        Finds the number of duplications for each
        available component in a column

        Parameters
        ----------
        column : str
            the name of the column in the database where
            the operation should happen
        database : str
            the name of the database where the operation 
            should happen

        Returns
        -------
        list_of_duplicates : list
            containts the column_variable in first column and
            the number of duplications in second column
        """
        self.cur.execute("SELECT " + column + ", COUNT( " + column + " ) c from " + database + " GROUP BY " + column + " ORDER BY c DESC")
        list_of_duplicates = self.cur.fetchall()
        return [[list_of_duplicates[0], list_of_duplicates[1]] for list_of_duplicates in list_of_duplicates]

    def __del__(self):
        """
        Destroys instance and connection on completion of called method 
        """
        self.conn.close()


class ListingDataBase(DataBase):
    def __init__(self, output_directory):
        DataBase.__init__(self, output_directory)
        self.cur.execute(
            "CREATE TABLE Listings (id INT, make STRING, price REAL, mileage REAL, seller_type STRING);")

    def insert_csv_into_db(self, input_directory):
        """
        Reads the csv file then inserts the data into the listing.db file
        """
        with open(input_directory, 'r') as csv_file:
            dr = csv.DictReader(csv_file)
            to_db = [(i['id'], i['make'], i['price'],
                      i['mileage'], i['seller_type']) for i in dr]

        self.cur.executemany(
            "INSERT INTO Listings (id, make, price, mileage, seller_type) VALUES (?, ?, ?, ?, ?);", to_db)
        self.conn.commit()


class ContactsDataBase(DataBase):
    def __init__(self, output_directory):
        DataBase.__init__(self, output_directory)
        self.cur.execute(
            "CREATE TABLE Contacts (listing_id INT, contact_date INT);")

    def insert_csv_into_db(self, input_directory):
        """
        Reads the csv file then inserts the data into the contacts.db file
        """
        with open(input_directory, 'r') as csv_file:
            dr = csv.DictReader(csv_file)
            to_db = [(i['listing_id'], i['contact_date']) for i in dr]

        to_db = Operations.convert_contact_date_to_readable_format(to_db)

        self.cur.executemany(
            "INSERT INTO Contacts (listing_id, contact_date) VALUES (?, ?);", to_db)
        self.conn.commit()
        