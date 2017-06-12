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
        user_input = input("-> ")
    budget_limit = compute_budget_total(CATEGORIES)
    budget = Budget(budget_limit, TRANSACTIONS, CATEGORIES)
    print("Leaving budget setup...")
    budget_view(budget)


def budget_view(budget):
    print("Opening budget view...")

    user_input = input("-> ").lower()
    while(user_input != "home"):
        if user_input == "add transaction":
            add_transaction(budget)
        elif user_input == "view transactions":
            print(pandas.DataFrame(
                budget.transactions.all()).set_index("id"))
        elif user_input == "view status":
            if (budget.over_total_budget()):
                print("You are over your budget.")
            else:
                print("Your spending has been in budget!")
        user_input = input("-> ").lower()

    print("Closing budget view...")

def add_transaction(budget):
    print("You can add a transaction by inputting"
          "the price of the transaction, the category"
          "it falls under, and the date of the transaction,"
          " all separated by commas. Enter done when you are"
          " finished adding transactions.")
    user_input = input("-> ")
    while user_input != "done":
        transaction_data = user_input.split(",")
        cost = float(transaction_data[0])
        category = transaction_data[1]
        date = transaction_data[2]
        verify_category = budget.categories.search(
            QUERY.name == category)
        if len(verify_category) > 0:
            new_transaction = Transaction(
                cost,category,date)
            budget.transactions.insert(new_transaction.__dict__)
        else:
            print("That category has not been created, try again.")
        user_input = input("-> ")
    print("Returning to budget view")


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

def update(budget):
    print("Budget total is: $" + "{0:.2f}".format(budget.get_limit()))
    for i in range(1, len(CATEGORIES) + 1):
        category = CATEGORIES.search(QUERY.id == i)[0]
        category_name = category['name']
        category_limit = category['limit']
        print("{}'s limit is ${}".format(category_name,
                                         category_limit))

    print ("Total spent is: " + "${0:.2f}".format(budget.total_spent))

def clear():
    CATEGORIES.purge_tables()
    TRANSACTIONS.purge_tables()


CATEGORIES = None
TRANSACTIONS = None
QUERY = Query()
main_menu()