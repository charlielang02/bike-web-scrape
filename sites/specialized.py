import requests
from bs4 import BeautifulSoup

def get_user_input(prompt):
    return input(prompt + " (leave blank to skip): ").strip()

category = get_user_input("Enter category (e.g., Mountain):")
product_family = get_user_input("Enter product family (e.g., Rockhopper):")

URL = "https://www.specialized.com/ca/en/c/bikes?"
i = 1
if category:
    URL += f"categoryproperty={category}&"
if product_family:
    URL += f"productfamily={product_family}&"
base_url = URL
print(f"\nSearching at {URL}\n")

results = []
while True:
    try:
        URL = base_url + f"page={i}"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
    except Exception as e:
        print("An error occurred:", e)
        break

    if not soup.find(class_="sc-19235d64-0 fnaHls"):
        break

    results += soup.find_all(class_="sc-19235d64-0 fnaHls")
    i += 1

all_results = BeautifulSoup("", "html.parser")
for result in results:
    all_results.append(result)

models = all_results.find_all("li")
for model in models:
    if not model.get("class"):
        model_name_tag = model.find("a", class_="sc-1592a746-6 dvBYsj")
        model_price_tag = model.find("div", class_="sc-1592a746-5 bMkAuT")
        if model_name_tag:
            model_name = model_name_tag.text.strip()
        else:
            model_name = "Name not found"
        if model_price_tag:
            model_price = model_price_tag.find("span").text.strip()
        else:
            model_price = "Price not found"
        print(model_name)
        print(model_price)
        print()