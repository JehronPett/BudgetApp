import pandas
from tinydb import TinyDB, Query
from Structure.Budget import Budget
from Structure.Category import Category
from Structure.Transaction import Transaction


def main_menu():
    """
    The main menu of this app, with four commands.
    'add new budget' : start a new budget
    'view budget' : view the current budget
    """
    print("Welcome to the Budget App.")
    print("What would you like to do?")
    user_input = input("-> ").lower()
    while user_input != "quit":
        if user_input == "add new budget":
            budget_setup()
        elif user_input == "view budget":
            CATEGORIES = TinyDB("Backend/categories.json")
            TRANSACTIONS = TinyDB("Backend/transactions.json")
            budget_limit = Budget.compute_budget_total(CATEGORIES)
            budget_view(Budget(budget_limit, TRANSACTIONS, CATEGORIES))
        else:
            print("I do not recognize that command. Try again")
        user_input = input("-> ").lower()
    print("Goodbye.")

def budget_setup():
    """
    The budget setup window. The budget is created here by
    creating categories and limits, and adding
    them to our categories database. We also
    initialize our budget object here.
    """
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
    budget_limit = Budget.compute_budget_total(CATEGORIES)
    budget = Budget(budget_limit, TRANSACTIONS, CATEGORIES)
    print("Leaving budget setup and opening budget view...")
    budget_view(budget)

def budget_view(budget):
    """
    This is the budget view, with four commands.
    'transactions view' : open the transactions window
    'view status' : view the status of the budget
    'edit budget' : add or remove categories
    'done' : close budget view
    """
    print("Opening budget view...")
    user_input = input("-> ").lower()
    while(user_input != "done"):
        if user_input == "transactions view":
            transactions_view(budget)
        elif user_input == "view status":
            view_status(budget)
            if (budget.over_total_budget()):
                print("You are over your budget. You're bugging out.")
            else:
                print("Your spending has been in budget. Keep it up.")
        elif user_input == "edit budget":
            edit_budget(budget)
        else:
            print("I do not recognize that command. Try again")
        user_input = input("-> ").lower()
    print("Closing budget view and returning to main menu...")

def transactions_view(budget):
    """
    This is the transactions view, with three commands.
    'add transactions' : add a new transaction
    'view transactions' : view all transactions
    'remove transactions' : remove a transaction
    'done' : return to budget view
    """
    print("Opening transactions view...")
    user_input = input("-> ").lower()
    while user_input != "done":
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
        else:
            print("I do not recognize that command. Try again.")
        user_input = input("-> ")
    print("Closing transactions view and returning to budget view...")

def edit_budget(budget):
    """
    The edit budget menu, with three commands.
    'add' : add a new category
    'remove' : remove a category
    'done' : return to the main menu

    :param budget: the current budget
    :return: None
    """
    print("In edit budget view...")
    print("Would you like to add or delete a category?")
    user_input = input("-> ").lower()
    while user_input != "done":
        if user_input == "add":
            add_category(budget.categories)
        elif user_input == "delete":
            print("Please enter the names of the category you "
                  "would like to delete.")
            remove_category(budget.categories)
        else:
            print("I do not recognize that command.")
        user_input = input("-> ").lower()
    print("Leaving edit budget view and returning to the budget view...")

def add_category(category_db):
    """
    This is the functionality for adding a category in the edit
    budget view.
    """
    print("Please enter a category by entering the "
          "name of the category and its limit, "
          "separated by a comma like this: Food,20.0")
    user_input = input("-> ").lower()
    while user_input != "done":
        string_list = user_input.split(",")
        category = Category(string_list[0], float(string_list[1]))
        category_db.insert(category.__dict__)
        user_input = input("-> ").lower()

def remove_category(category_db):
    """
    This is the functionality for deleting a category in the
    edit budget view.
    """
    # TODO: When deleting a category, delete all transactions that fall under it
    print("Please enter the name of the category you would like to remove")
    category_to_delete = input("-> ")
    while category_to_delete != "done":
        find_category = category_db.search(QUERY.name == category_to_delete)
        if len(find_category) == 1:
            category_db.remove(QUERY.name == category_to_delete)
            print("Successfully removed the "
                  "'{}' category".format(category_to_delete))
        else:
            print("Hmm... I couldn't find that category.")
        category_to_delete = input("-> ")
    print("Returning to edit budget view...")

def view_status(budget):
    """
    This is the budget status view. Here we can see exactly
    what we've spent in each category, and it's respective
    limit. We are also notified if we are over or under
    the budget.
    """
    print()
    print("Your Budget limit: $" + "{0:.2f}".format(budget.get_limit()))
    print()
    list_of_categories = budget.categories.all()
    for i in range(len(list_of_categories)):
        category = list_of_categories[i]
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
    """
    This is the functionality for adding a transaction to
    our budget transactions database.
    """
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
    """
    This is the functionality for removing a transaction from
    our budget transactions database.
    """
    print("This functionality has not been implemented yet")


CATEGORIES = None
TRANSACTIONS = None
QUERY = Query()
main_menu()