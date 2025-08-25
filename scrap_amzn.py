import os
import time
import smtplib
import sqlite3
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

DB_FILE = os.path.join(os.getcwd(), "products.db")

""" Import environment variables """
load_dotenv()
smtp_addr = os.getenv("SMTP_ADDRESS")
email_addr = os.getenv("EMAIL_ADDRESS")
email_passwd = os.getenv("EMAIL_PASSWORD")

""" Retrieve data from the database """
def fetch_db_data():
    # Connect to the database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    results = cursor.execute("SELECT nickname, product_url, target_price FROM amazon_products")

    # Store the data in a list
    products_data = [result for result in results.fetchall()]

    # Commit changes and disconnect from the database
    conn.commit()
    conn.close()
    return products_data  # Return the list of products

""" Open browser, get product data from website, and send notification according to logic """
def scrap_amazon(nickname: str, product_link: str, target_price: float):
    # 1. Start Chrome browser with headless behavior
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    driver.get(url=product_link)
    time.sleep(5)

    # 2. Fetch the name and current pricing of the product
    try:
        print("[*] Retrieving the name and current price of the product")

        item_name = driver.find_element(By.ID, value="titleSection").text
        price_dollars = driver.find_element(By.CLASS_NAME, value="a-price-whole").text
        price_cents = driver.find_element(By.CLASS_NAME, value="a-price-fraction").text
        current_price = float(f"{price_dollars}.{price_cents}")  # convert price to a floating number

        # 3. Send an email if the price has dropped
        if current_price > target_price:
            print(f"[X] No lower price found for {nickname}. Moving on to next product if any.")

        else:
            print(f"[*] {nickname} has a lower price. Sending notification...")
            message = f"Product: {item_name}\n \
            Current price: ${current_price}\n \
            Link: {product_link}\n"

            # 4. Establish a secure SMTP connection and log user credentials
            with smtplib.SMTP(smtp_addr, port=587) as connection:
                connection.starttls()
                connection.login(user=email_addr, password=email_passwd)

                connection.sendmail(
                    from_addr=email_addr,
                    to_addrs=email_addr,
                    msg=f"Subject: {nickname} has a lower price\n\
                                        {message}".encode("utf-8")
                )
            print("[+] Email has been sent.")

    except Exception as e:
        print(f"⚠️ Error: {e}")

    finally:
        driver.quit()  # Close the browser

""" Main program to be executed """
def main():
    print("[*] Opening web browser...")

    products_data = fetch_db_data()
    for i in range(0, len(products_data)):
        scrap_amazon(products_data[i][0],  # Product's nickname
                     products_data[i][1],  # Product URL
                     products_data[i][2]  # Product's target price
                     )
        print()
        time.sleep(5)
    print("[*] Closing web browser.")


if __name__ == "__main__":
    main()