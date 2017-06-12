from tinydb import TinyDB, Query


class Budget:
    """
    An instance of this object holds information about
    everything regarding this budget
    """
    def __init__(self, limit, transactions, categories):
        """
        Initialize this budget object with the limit,
        and databases of categories and transactions
        :param limit: the overall budget limit
        :type limit: float
        :param transactions: the database of
                            transactions
        :type transactions: TinyDB
        :param categories: the database of categories
        :type categories: TinyDB
        """
        self.limit = limit
        self.transactions = transactions
        self.categories = categories

    def get_limit(self):
        """
        Getter method for the limit field
        :return: limit
        """
        return self.limit

    def get_transactions(self):
        """
        Getter method for the transactions database
        :return: transactions database
        """
        return self.transactions

    def get_categories(self):
        """
        Getter method for the categories database
        :return: categories database
        """
        return self.categories

    def total_spent(self):
        """
        Compute the total amount of money spent
        :return: the dollar total of all transactions
        """
        sum = 0
        for i in range(len(self.transactions)):
            current = self.transactions.all()[i]
            sum += current['cost']
        return sum

    def over_total_budget(self):
        """
        :return: True if we are over our total budget,
                    False otherwise
        """
        return self.total_spent() > self.get_limit()

    def over_category_budget(self, category):
        """
        Find out if I am over budget in the specified category
        :param category: self-explanatory
        :type category: str
        :return: true if we are, false otherwise
        """
        category_totals = self.category_totals()
        category_limit = self.category_limit(category)
        return category_totals[category] > category_limit

    def category_limit(self, category):
        return self.categories.search(
            Query().name == category)[0]['limit']


    def category_total(self, category):
        transactions_in_category = self.transactions.search(
            Query().category == category)
        category_total_sum = 0
        for i in range(len(transactions_in_category)):
            category_total_sum += transactions_in_category[i]['cost']
        return category_total_sum

    def category_totals(self):
        """
        Compute the total amount spent in each category
        :return: a dictionary where the keys are the
                    categories and the values are the
                    totals
        """
        category_totals = {}
        for i in range(len(self.categories)):
            current_category = self.categories.all()[i]['name']
            transactions_in_category = self.transactions.search(
                Query().category == current_category)
            category_total_sum = 0
            for i in range(len(transactions_in_category)):
                category_total_sum += transactions_in_category[i]['cost']
            category_totals[current_category] = category_total_sum
        return category_totals


    def set_limit(self, new_limit):
        """
        Modify this budget's limit
        :param new_limit: the new limit
        :return: None
        """
        self.limit = new_limit
