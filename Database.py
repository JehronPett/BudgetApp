import tinydb as database

class Database:
    """
    Database class that can hold objects
    """
    def __init__(self, name):
        """
        Initialize the new database
        :param name: the name of this database
        """
        db_file = open("{}.json".format(name), "w+")
        self.db = database.TinyDB('{}'.format(db_file.name))

    def insert(self, new_row):
        """
        Insert a new transaction into the database
        :param new_row: self-explanatory
        :type new_row: object
        :return: None
        """
        self.db.insert(new_row.__dict__)

    @property
    def show_table(self):
        return self.db.all()

