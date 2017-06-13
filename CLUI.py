import pandas
from tinydb import TinyDB, Query

from Structure.Budget import Budget
from Structure.Category import Category
from Structure.Transaction import Transaction


def main_menu():
    print("Welcome to the Budget App.")
    print("What would you like to do?")
    user_input = input("-> ").lower()
    while (user_input != "quit"):
        # TODO: Implement the remove category functionality
        if user_input == "add new budget":
            budget_setup()
        elif user_input == "view budget":
            CATEGORIES = TinyDB("Backend/categories.json")
            TRANSACTIONS = TinyDB("Backend/transactions.json")
            budget_limit = compute_budget_total(CATEGORIES)
            budget_view(Budget(budget_limit, TRANSACTIONS, CATEGORIES))
        elif user_input == "edit budget":
            CATEGORIES = TinyDB("Backend/categories.json")
            TRANSACTIONS = TinyDB("Backend/transactions.json")
            budget_limit = compute_budget_total(CATEGORIES)
            edit_budget(Budget(budget_limit, TRANSACTIONS, CATEGORIES))
        else:
            print("I do not recognize that command. Try again")
        user_input = input("-> ").lower()
    print("Goodbye.")

def edit_budget(budget):
    print("In edit budget view...")
    print("Would you like to add or delete a category?")
    user_input = input("-> ").lower()
    while user_input != "done":
        if user_input == "add":
            add_categories(budget.categories)
        elif user_input == "delete":
            print("Please enter the names of the category you "
                  "would like to delete.")
            delete_categories(budget.categories)
        else:
            print("I do not recognize that command.")
        user_input = input("-> ").lower()

    print("Leaving edit budget view and returning to main menu...")


def budget_setup():
    # TODO: Set up a structure that allows me to input my initial budget limit, then fill out categories after
    # This should allow for an "Extra" category of the budget which has a limit that evaluates to the
    # total budget limit minus the sum of the category limits
    print("In budget setup...")
    db_file = open("Backend/{}.json".format("categories"), "w+")
    CATEGORIES = TinyDB('{}'.format(db_file.name))
    db_file = open("Backend/{}.json".format("transactions"), "w+")
    TRANSACTIONS = TinyDB('{}'.format(db_file.name))
    print("Now let's add the spending categories of this budget.")
    add_categories(CATEGORIES)
    budget_limit = compute_budget_total(CATEGORIES)
    budget = Budget(budget_limit, TRANSACTIONS, CATEGORIES)
    print("Leaving budget setup and returning to main menu...")
    budget_view(budget)

def add_categories(category_db):
    print("Please enter a category by entering the "
          "name of the category and its limit, "
          "separated by a comma like this: Food,20.0")
    user_input = input("-> ").lower()
    while user_input != "done":
        string_list = user_input.split(",")
        category = Category(string_list[0], float(string_list[1]))
        category_db.insert(category.__dict__)
        user_input = input("-> ").lower()

def delete_categories(category_db):
    print("This functionality has not been implemented yet.")

def budget_view(budget):
    print("Opening budget view...")
    user_input = input("-> ").lower()
    while(user_input != "done"):
        if user_input == "add transactions":
            add_transaction(budget)
        elif user_input == "view transactions":
            if len(budget.transactions) > 0:
                print(pandas.DataFrame(
                    budget.transactions.all()).set_index("id"))
            else:
                print("I could not find any transactions to display.")
        elif user_input == "remove transactions":
            # TODO: Implement the remove transaction method
            remove_transaction(budget)
        elif user_input == "view status":
            view_status(budget)
            if (budget.over_total_budget()):
                print("You are over your budget. You're bugging out.")
            else:
                print("Your spending has been in budget. Keep it up.")
        else:
            print("I do not recognize that command. Try again")
        user_input = input("-> ").lower()

    print("Closing budget view and returning to main menu...")

def view_status(budget):
    print()
    print("Your Budget limit: $" + "{0:.2f}".format(budget.get_limit()))
    print()
    for i in range(len(budget.categories)):
        category = budget.categories.search(QUERY.id == i)[0]
        category_name = category['name']
        category_limit = category['limit']
        print("{}'s limit: $".format(category_name) +
              "{0:.2f}".format(category_limit))
        category_total = budget.category_total(category_name)
        print("Total spending in {}'s category: ".format(category_name) +
              "${0:.2f}".format(float(category_total)))
        print()

    print("Total spending amounts to: " + "${0:.2f}".format(budget.total_spent()))

def add_transaction(budget):
    print("You can add a transaction by inputting")
    print("the price of the transaction, the category")
    print("it falls under, and the date of the transaction,")
    print("all separated by commas. Enter done when you are")
    print("finished adding transactions.")
    user_input = input("-> ").lower()
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
        user_input = input("-> ").lower()
    print("Returning to budget view...")

def remove_transaction(budget):
    print("This functionality has not been implemented yet")

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


CATEGORIES = None
TRANSACTIONS = None
QUERY = Query()
main_menu()