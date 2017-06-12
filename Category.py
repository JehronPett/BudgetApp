class Category:
    """
    An instance of this object simply represents a single
    category of the budget and it's spending limit.
    """
    ID = 0

    def __init__(self, name, limit):
        """
        Initialize a new Category object
        :param name: the name of this category
        """
        self.limit = limit
        self.name = name
        self.id = Category.ID
        Category.ID += 1

    def get_name(self):
        """
        :return: the name of this category
        """
        return self.name

    def get_id(self):
        """
        :return: the id of this category
        """
        return self.id

    def get_limit(self):
        """
        :return: the spending limit of this category
        """
        return self.limit

    def set_name(self, new_name):
        """
        :param new_name: the new name of this category
        :return: None
        """
        self.name = new_name

    def set_limit(self, new_limit):
        """
        :param new_limit: the new spending limit of this
                            category
        :return: None
        """
        self.limit = new_limit