import os, time, smtplib
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Add as many products as needed
PRODUCTS = {
    "product1": {
        "the_url": "",
        "target_price": 0.00,
    },
    "product2": {
        "the_url": "",
        "target_price": 0.00,
    },
    "product3": {
        "the_url": "",
        "target_price": 0.00,
}

""" Import environment variables """
load_dotenv()
smtp_addr = os.getenv("SMTP_ADDRESS")
email_addr = os.getenv("EMAIL_ADDRESS")
email_passwd = os.getenv("EMAIL_PASSWORD")

""" Open browser, get product data from website, and send notification according to logic """
def scrap_microcenter(the_url:str, target_price: float):
    # 1. Launch Chrome browser in headless mode
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    driver.get(url=the_url)
    driver.implicitly_wait(5)

    # 2. Fetch the name and current pricing of the product
    try:
        print("🔃 Retrieving the name and current price of the product")

        product_name = driver.find_element(By.CLASS_NAME, value="product-header").text
        current_price_str = driver.find_element(By.CLASS_NAME, value="big-price").text
        current_price = float(current_price_str.split("$")[1])

        # 3. Send an email if the price has dropped
        if current_price > target_price:
            print(f"❌ No lower price found for {product_name}")

        else:
            print(f"✅ Lower price found. Sending notification...")
            message = f"Product: {product_name}\n\
            Current price: ${current_price}\n\
            Link: {the_url}"

            # 4. Establish a secure SMTP connection, log user credentials and send email
            with smtplib.SMTP(smtp_addr, port=587) as connection:
                connection.starttls()
                connection.login(user=email_addr, password=email_passwd)
                connection.sendmail(
                    from_addr=email_addr,
                    to_addrs=email_addr,
                    msg=f"Subject: Your item has a lower price\n{message}".encode("utf-8"),
                )
            print("✅ Email has been sent.")

    except Exception as e:
        print(f"⚠️ Error: {e}")

    finally:
        print("Closing browser...")
        driver.quit()  # Close the browser

def main():
    for key in list(PRODUCTS.keys()):
        scrap_microcenter(the_url=PRODUCTS[key]["the_url"],
                          target_price=PRODUCTS[key]["target_price"])
        time.sleep(3)   # Wait for 3 second before checking the next item

if __name__ == "__main__":
    main()
