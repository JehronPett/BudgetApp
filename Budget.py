from Transaction import Transaction
from Category import Category
from Database import Database
import tinydb
import pandas

class Budget:
    def __init__(self, limit):
        self.limit = limit
    def get_limit(self):
        return self.limit
    def set_limit(self, new_limit):
        self.limit = new_limit

def main():
    category_one = Category("Food", 20.00)
    transaction_one = Transaction("19.78,Food,060317")
    transaction_two = Transaction("2.35,Food,060417")
    CATEGORIES.insert(category_one)
    TRANSACTIONS.insert(transaction_one)
    TRANSACTIONS.insert(transaction_two)
    print(CATEGORIES.show_table)
    print(TRANSACTIONS.show_table)
    budget = Budget(1000.0)
    update(budget)

def update(budget):
    print("Budget total is: " + str(budget.get_limit()))
    print("Length of db is: " + str(len(CATEGORIES.db)))
    for i in range(1, len(CATEGORIES.db) + 1):
        db = CATEGORIES.db
        category = db.search(QUERY.id == i)[0]
        category_name = category['name']
        category_limit = category['limit']
        print("{}'s limit is ${}".format(category_name,
                                         category_limit))
    print (pandas.DataFrame(TRANSACTIONS.show_table))



def clear():
    CATEGORIES.clear()
    TRANSACTIONS.clear()


CATEGORIES = Database("categories")
TRANSACTIONS = Database("transactions")
QUERY = tinydb.Query()
#clear()
main()