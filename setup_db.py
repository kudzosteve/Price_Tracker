import os
import sqlite3
import requests
from urllib.parse import urlparse
from sqlite3 import IntegrityError

DB_FILE = os.path.join(os.getcwd(), "products.db")

def valid_url(product_url):
    """ Check if the given URL is well-formed """
    parsed_url = urlparse(url=product_url)
    if all([parsed_url.scheme, parsed_url.netloc]):
        return True

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/;q=0.8'
    }

    """ Check if the given url is reachable """
    try:
        response = requests.get(url=product_url, headers=headers, timeout=5)
        return response.status_code in [200, 201]
    except requests.RequestException:
        return False

def create_db():
    """ Create 'products' database to store items' data """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS amzn_products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nickname TEXT,
        product_url TEXT NOT NULL UNIQUE,
        target_price REAL NOT NULL
    );
    """)

    conn.commit()
    conn.close()

def add_items(nickname:str, prod_url:str, target_price:float):
    """ Add items to the database """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO amzn_products (nickname, product_url, target_price) VALUES (?,?,?)",
                       (nickname, prod_url, target_price))
        conn.commit()
    except IntegrityError:
        print(f"[X] Duplicate URL detected for {nickname}. Skipping...")
    finally:
        conn.close()


if __name__ == "__main__":
    print("[*] Setting up the database...")
    if not os.path.isfile(DB_FILE):
        create_db()

    while True:
        try:
            num_products = int(input("[?] How many products do you need to add to the database? "))
            break
        except ValueError:
            print("[X] Invalid input! Try again!")

    for n in range(1, num_products + 1):
        print(f"Product No. {n}")
        while True:
            url = input("[*] Paste the url of product: ")
            if valid_url(url):
                break
            else:
                print("[X] Invalid or unreachable URL. Please try again.")
        while True:
            try:
                target_price = float(input("[*] Input your desired price: "))
                break
            except ValueError:
                print("[X] Invalid price. Please enter a number.")
        nickname = input("[*] Set a nickname for your product (this will be used as the email's subject): ").title()
        add_items(nickname, url, target_price)
        print()
    print("[+] Database has been updated.")