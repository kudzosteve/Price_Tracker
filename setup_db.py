import os
import sqlite3
import requests
from urllib.parse import urlparse
from sqlite3 import IntegrityError

DB_FILE = os.path.join(os.getcwd(), "products.db")
TABLES = {
    "1": "amazon_products",
    "2": "microcenter_products",
}

""" Function that checks if the url is well formed and reachable """
def valid_url(product_url):
    # Check if the given URL is well-formed
    parsed_url = urlparse(url=product_url)
    if all([parsed_url.scheme, parsed_url.netloc]):
        return True

    # Headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/;q=0.8'
    }

    # Check if the URL can be reached
    try:
        response = requests.get(url=product_url, headers=headers, timeout=5)
        return response.status_code in [200, 201]
    except requests.RequestException:
        return False

""" Functions that creates 'products' database to store items data """
def create_db():
    # Create a connection to the database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create a table for Amazon products
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS amazon_products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nickname TEXT,
        product_url TEXT NOT NULL UNIQUE,
        target_price REAL NOT NULL
    );
    """)

    # Create a table for Microcenter products
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS microcenter_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT,
            product_url TEXT NOT NULL UNIQUE,
            target_price REAL NOT NULL
        );
        """)

    # Commit changes and close the connection to the database
    conn.commit()
    conn.close()

""" Function that insert values into the tables of the database """
def add_items(the_table:str, nickname:str, prod_url:str, target_price:float):
    # Create a connection to the database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        # Insert values to the table and commit changes to the database
        cursor.execute(f"INSERT INTO {the_table} (nickname, product_url, target_price) VALUES (?,?,?)",
                       (nickname, prod_url, target_price))
        conn.commit()
    except IntegrityError:
        print(f"[X] Duplicate URL detected for {nickname}. Skipping...")
    finally:
        conn.close()    # Close the connection

""" Function that receives user inputs and updates the database """
def update_database(the_table):
    # Create the database if it does not exist in current working directory
    print("[*] Setting up the database...")
    if not os.path.isfile(DB_FILE):
        create_db()

    # use a continuous loop to receive user input
    while True:
        # Get the number of products
        try:
            num_products = int(input("[?] How many products do you need to add to the database? "))
            break
        except ValueError:
            print("[X] Invalid input! Try again!")

    for n in range(1, num_products + 1):
        print(f"Product No. {n}")

        while True:     # Get the URL
            url = input("[*] Paste the url of product: ")
            if valid_url(url):
                break
            else:
                print("[X] Invalid or unreachable URL. Please try again.")

        while True:     # Get a price threshold
            try:
                target_price = float(input("[*] Input your desired price: "))
                break
            except ValueError:
                print("[X] Invalid price. Please enter a number.")

        # Get a nickname for the product
        nickname = input("[*] Set a nickname for your product (this will be used in the email's subject): ").title()

        add_items(the_table, nickname, url, target_price)
        print()
    print("[+] Database has been updated.")

""" Function to execute all the functions """
def execute_program():
    run_code = True
    invalid_input = 3

    while run_code:
        print("What marketplace products do you want to add?\n \
        [1] Amazon\n \
        [2] Microcenter")
        while True:     # Get the appropriate key for the right table
            try:
                table = input("Enter 1 or 2: ")
                if table in ('1', '2'):
                    break
                else:
                    # Limit invalid inputs to 3 attempts before exiting the program
                    invalid_input -= 1
                    if invalid_input != 0:
                        print("[!] Invalid input. Please enter 1 or 2")
                    else:
                        print("[] Three invalid inputs detected. Exiting program.")
                        exit()
                    continue
            except ValueError:
                print("[!] Invalid input. Try again")

        update_database(TABLES[table])      # Update the desired table in the database with new information

        # Should the program continue?
        ask = input("[*] Do you want to add more items to a database? [y]es or [n]o: ")
        if ask in ("yes", "y"):
            continue
        else:
            run_code = False    # Stop code execution

if __name__ == "__main__":
    execute_program()