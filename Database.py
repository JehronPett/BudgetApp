class Database:
    """
    Database class that can hold objects
    """
    def __init__(self):
        """
        Initialize the new database
        """
        self.db = []

    def insert(self, new_row):
        """
        Insert a new transaction into the database
        :param new_transaction: self-explanatory
        :return: None
        """
        self.db.append(new_row)

    def remove(self, old_row):
        """
        Remove an old_transaction
        :param old_transaction: self-explanatory
        :return: None
        """
        self.db.remove(old_row)

    def select(self, row_id):
        """
        Access a old transaction object by ID
        :param old_transaction: self-explanatory
        :return: the specified transaction
        """
        return self.db[row_id]

