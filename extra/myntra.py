from selenium import webdriver
from bs4 import BeautifulSoup

# Initialize Firefox WebDriver
driver = webdriver.Firefox()

# URL of the Myntra men topwear page
url = 'https://www.myntra.com/men-topwear'
driver.get(url)

# Get the page source using Selenium
page_source = driver.page_source

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Find all <li> elements with class "product-base"
product_list = soup.find_all('li', class_='product-base')

# Extract and print product names
for product in product_list:
    product_brand_element = product.find('h4', class_='product-brand') 
    product_name_element = product.find('h4', class_='product-product')
    if product_name_element:
        product_name = product_name_element.text.strip()
        print("Product Name: ", product_name)

        # Extract the link for the product page
        product_link_element = product.find('a', href=True)
        if product_link_element:
            product_link = product_link_element['href']

            # Visit the individual product page
            driver.get("https://www.myntra.com/" + product_link)

            # Get the page source of the individual product page
            product_page_source = driver.page_source

            # Parse the individual product page source with BeautifulSoup
            product_soup = BeautifulSoup(product_page_source, 'html.parser')

            # Extract and print the product title from the individual product page
            product_title_element = product_soup.find('h1', class_='pdp-title')
            if product_title_element:
                product_title = product_title_element.text.strip()
                print("Product Title:", product_title)

            # Add any other information you want to extract from the individual product page
            # For example, price, ratings, description, etc.

            # Go back to the main page to visit the next product page
            driver.back()
            print("Visited product page and back to the main page.\n")

# Close the browser
driver.quit()
