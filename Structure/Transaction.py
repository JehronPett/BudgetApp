class Transaction:
    """
    Any instance of this class contains information
    for a transaction such as the cost, the budget
    category it resides in, and the date of the
    transaction.
    """
    ID = 0

    def __init__(self, cost, category, date):
        """
        Initialize a new transaction to be
        documented

        :param cost: The total cost of this
                        transaction
        :type cost: float
        :param category: The category of the
                        budget this transaction
                        falls under
        :type category: str
        :param date: The date of this transaction
        :type date: str
        """
        self.cost = cost
        self.category = category
        self.date = date
        self.id = Transaction.ID
        Transaction.ID += 1

    def get_cost(self):
        """
        :return: the cost of this transaction
        """
        return self.cost

    def get_category(self):
        """
        :return: the category of this transaction
        """
        return self.category

    def get_date(self):
        """
        :return: the date of this transaction
        """
        return self.date

    def get_id(self):
        """
        :return: the id of this transaction
        """
        return self.id

    def set_cost(self, new_cost):
        """
        :param newCost: the new cost of this transaction
        :return: None
        """
        self.cost = new_cost

    def set_category(self, new_category):
        """
        :param newCategory: the new category of this transaction
        :return: None
        """
        self.category = new_category

    def set_date(self, new_date):
        """
        :param newDate: the new date of this transaction
        :return: None
        """
        self.date = new_date
