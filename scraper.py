from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Selenium WebDriver
options = Options()
# options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

# Rotate User-Agent to prevent detection
ua = UserAgent()
options.add_argument(f"user-agent={ua.random}")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Target website
URL = "https://www.ebay.com/globaldeals/tech"

wait = WebDriverWait(driver, 2)

def scroll_down():
    """ Scroll down the page to load all items (handles lazy loading) """
    last_height = driver.execute_script("return document.body.scrollHeight")

    for _ in range(5):  # Scroll down multiple times
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Give time for new elements to load
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break  # Stop scrolling if no new content loads
        last_height = new_height
def scrape_ebay_data():
    """Scrape tech deals from eBay Global Deals page."""
    driver.get(URL)
    time.sleep(15)  # Allow time for page load
    scroll_down()  # Scroll to load all products

    try:
        products = []
        items = driver.find_elements(By.XPATH, "//div[contains(@class, 'dne-itemtile-detail')]")
        print(len(items))
        for item in items[:30]:
            try:
                title = item.find_element(By.XPATH, ".//h3[contains(@class,'dne-itemtile-title')]").text
            except:
                title = "N/A"

            try:
                price = item.find_element(By.XPATH, ".//div[@itemprop='offers']").text
            except:
                price = "N/A"

            try:
                original_price = item.find_element(By.XPATH, ".//span[@class='itemtile-price-strikethrough']").text
            except:
                original_price = "N/A"

            try:
                item_url = wait.until(EC.presence_of_element_located(
                    (By.XPATH, ".//div[@class='dne-itemtile-detail']//a"))).get_attribute("href")
            except:
                item_url = "N/A"

            try:
                shipping = wait.until(EC.presence_of_element_located(
                    (By.XPATH, ".//span[contains(@class, 'dne-itemtile-delivery')]"))).text
            except:
                shipping = "N/A"

            # Capture timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            products.append([timestamp, title, price, original_price, shipping, item_url])

        return products

    except Exception as e:
        print("Error:", e)
        return []


def save_to_csv(data, filename="ebay_tech_deals.csv"):
    """Save scraped data to CSV."""
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["timestamp", "title", "price", "original_price", "shipping", "url"])

    new_data = pd.DataFrame(data, columns=["timestamp", "title", "price", "original_price", "shipping", "url"])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(filename, index=False)


if __name__ == "__main__":
    print("Scraping eBay Tech Deals...")
    ebay_data = scrape_ebay_data()

    if ebay_data:
        save_to_csv(ebay_data)
        print("Data saved successfully.")

    driver.quit()
