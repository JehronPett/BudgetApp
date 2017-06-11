from Transaction import Transaction
from Category import Category
from Budget import Budget
from tinydb import TinyDB,Query
from Window import Window
import pandas


def main():
    # Create a category and two transactions for testing purposes
    category_one = Category("Food", 200.00)
    category_two = Category("Clothes", 300.00)
    transaction_one = Transaction(98.76,"Food","06/03/17")
    transaction_two = Transaction(345.01,"Clothes","06/04/17")
    transaction_three = Transaction(100.0,"Food","06/05/17")
    # Add these category and transaction objects to their
    # respective databases
    CATEGORIES.insert(category_one.__dict__)
    CATEGORIES.insert(category_two.__dict__)
    TRANSACTIONS.insert(transaction_one.__dict__)
    TRANSACTIONS.insert(transaction_two.__dict__)
    TRANSACTIONS.insert(transaction_three.__dict__)
    # Print these databases
    # print(CATEGORIES.all())
    # print(TRANSACTIONS.all())
    # Set Budget
    budget = Budget(500.0, TRANSACTIONS, CATEGORIES)
    update(budget)

def update(budget):
    print("Budget total is: $" + "{0:.2f}".format(budget.get_limit()))
    for i in range(1, len(CATEGORIES) + 1):
        category = CATEGORIES.search(QUERY.id == i)[0]
        category_name = category['name']
        category_limit = category['limit']
        print("{}'s limit is ${}".format(category_name,
                                         category_limit))
    print ()
    print ("Here are your transactions: ")
    print ()
    print (pandas.DataFrame(TRANSACTIONS.all()).set_index('id'))
    print ("Total spent is: " + "${0:.2f}".format(budget.total_spent))
    print (budget.over_total_budget())


def clear():
    CATEGORIES.purge_tables()
    TRANSACTIONS.purge_tables()

def gui():
    Window("Budget")


db_file = open("{}.json".format("categories"), "w+")
CATEGORIES = TinyDB('{}'.format(db_file.name))
db_file = open("{}.json".format("transactions"), "w+")
TRANSACTIONS = TinyDB('{}'.format(db_file.name))
QUERY = Query()

gui()