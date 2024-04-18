from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_user_input(prompt):
    return input(prompt + " (leave blank to skip): ").strip()

category = get_user_input("Enter category (e.g., Mountain):")
platform = get_user_input("Enter platform (e.g., Habit):")

URL = "https://www.cannondale.com/en-ca/bikes"
if category:
    URL += f"activeFilters=category~{category}|"
if platform:
    URL += f"platform~{platform}"

print(f"\nSearching at {URL}\n")

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run Chrome in headless mode
driver = webdriver.Chrome(options=options)

try:
    driver.get(URL)
    # Wait for products to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "product-details"))
    )
    soup = BeautifulSoup(driver.page_source, 'html.parser')
except Exception as e:
    print("An error occurred:", e)
finally:
    driver.quit()


# Now you can use BeautifulSoup to parse the fully rendered page source
product_cards = soup.find_all(class_="product-details")
if product_cards:
    for product_card in product_cards:
        product_name = product_card.find("h4", class_="product-card__title").text.strip()
        product_price = product_card.find("span", class_="product-card__price-sale")
        if not product_price:
            product_price = product_card.find("span", class_="product-card__price-main")
        product_price = product_price.text.strip()
        print(product_name)
        print(product_price)
        print()
else:
    print("No products found on the page.")
