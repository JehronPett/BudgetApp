from Transaction import Transaction
from Category import Category
from Budget import Budget
from tinydb import TinyDB,Query
import pandas


def main_menu():
    print("Welcome to the Budget App.")
    print("What would you like to do?")
    user_input = input("-> ")
    while (user_input != "quit"):
        if user_input.lower() == "new budget":
            budget_setup()
        elif user_input.lower() == "budget view":
            CATEGORIES = TinyDB("categories.json")
            TRANSACTIONS = TinyDB("transactions.json")
            budget_limit = compute_budget_total(CATEGORIES)
            budget_view(Budget(budget_limit, TRANSACTIONS, CATEGORIES))
        else:
            print("I do not recognize that command. Try again")
        user_input = input("-> ")
    print("Goodbye.")

def budget_setup():
    print("In budget setup...")
    db_file = open("{}.json".format("categories"), "w+")
    CATEGORIES = TinyDB('{}'.format(db_file.name))
    db_file = open("{}.json".format("transactions"), "w+")
    TRANSACTIONS = TinyDB('{}'.format(db_file.name))
    print("Let's add the budget categories. Please enter a category"
          "by entering the name of the category and its limit,"
          "separated by a comma like this: Food,20.0")
    user_input = input("-> ")
    while user_input != "done":
        string_list = user_input.split(",")
        category = Category(string_list[0], float(string_list[1]))
        CATEGORIES.insert(category.__dict__)
        user_input = input("->")
    budget_limit = compute_budget_total(CATEGORIES)
    budget = Budget(budget_limit, TRANSACTIONS, CATEGORIES)
    print("Leaving budget setup...")
    budget_view(budget)


def budget_view(budget):
    print("In budget view...")
    print("Leaving budget view...")

def compute_budget_total(categories):
    """
    Compute the total amount of this budget
    based on the total sum of the category
    limits
    :param categories: a database of categories
                        and their limits
    :type categories: TinyDB
    :return: the total budget
    """
    sum = 0
    for i in range(len(categories)):
        category = categories.search(QUERY.id == i)
        sum += float(category[0]['limit'])
    return sum

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


CATEGORIES = None
TRANSACTIONS = None
QUERY = Query()

main_menu()