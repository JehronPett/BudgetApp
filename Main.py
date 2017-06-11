from Transaction import Transaction
from Category import Category
from Database import Database

def main():
    category_one = Category("Food", 20.00)
    transaction_one = Transaction("19.78,Food,062517")
    CATEGORIES.insert(category_one)
    TRANSACTIONS.insert(transaction_one)
    print(CATEGORIES.show_table)
    print(TRANSACTIONS.show_table)


CATEGORIES = Database("categories")
TRANSACTIONS = Database("transactions")
main()