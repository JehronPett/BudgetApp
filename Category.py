class Category:
    """
    An instance of this object simply represents a single
    category of the budget.
    """
    ID = 0

    def __init__(self, name):
        """
        Initialize a new Category object
        :param name: the name of this category
        """
        self.name = name
        Category.ID += 1
        self.id = Category.ID

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

    def set_name(self, new_name):
        """
        :param new_name: the new name of this category
        :return: None
        """
        self.name = new_name
