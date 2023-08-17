from selenium import webdriver
from bs4 import BeautifulSoup

# Initialize Firefox WebDriver
driver = webdriver.Firefox()

# URL of the Myntra men topwear page
url = 'https://www.myntra.com/men-topwear'
driver.get(url)

# Get the page source using Selenium
page_source = driver.page_source

# Close the browser
driver.quit()

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Find all <li> elements with class "product-base"
product_list = soup.find_all('li', class_='product-base')

# Extract and print product names
for product in product_list:
    product_name_element = product.find('h4', class_='product-product')
    if product_name_element:
        product_name = product_name_element.text.strip()
        print(product_name)