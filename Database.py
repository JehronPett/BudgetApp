class Database:
    """
    Database object that will hold all transactions
    """
    def __init__(self):
        """
        Initialize a new database
        """
        self.transactions = []

    def insert(self, new_transaction):
        """
        Insert a new transaction into the database
        :param new_transaction: self-explanatory
        :return: None
        """
        self.transactions.append(new_transaction)

    def remove(self, old_transaction):
        """
        Remove an old_transaction
        :param old_transaction: self-explanatory
        :return: None
        """
        self.transactions.remove(old_transaction)

    def select(self, transaction_id):
        """
        Access a old transaction object by ID
        :param old_transaction: self-explanatory
        :return: the specified transaction
        """
        return self.transactions[transaction_id]