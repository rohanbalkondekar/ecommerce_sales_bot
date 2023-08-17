import csv
import os
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

# Extract and save product data to a CSV file
csv_file = 'myntra_products.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Product", "Product Info", "Product Rating", "Ratings Count", "Product Price", "Product Details", "Material and Care", "Specifications"])

    for product in product_list:
        product_data = []

        # Product Title
        product_title_element = product.find('h1', class_='pdp-title')
        if product_title_element:
            product_data.append(product_title_element.text.strip())

        # Product Info
        product_info_element = product.find('h1', class_='pdp-name')
        if product_info_element:
            product_data.append(product_info_element.text.strip())

        # Product Rating and Ratings Count
        product_rating_element = product.find('div', class_='index-overallRating')
        if product_rating_element:
            product_rating = product_rating_element.find('div').text.strip()
            product_ratings_count = product_rating_element.find('div', class_='index-ratingsCount').text.strip()
            product_data.append(product_rating)
            product_data.append(product_ratings_count)

        # Product Price
        product_price_element = product.find('span', class_='pdp-price')
        if product_price_element:
            product_data.append(product_price_element.text.strip())

        # Visit the individual product page
        product_link_element = product.find('a', href=True)
        if product_link_element:
            product_link = product_link_element['href']
            driver.get("https://www.myntra.com" + product_link)

            # Get the page source of the individual product page
            product_page_source = driver.page_source

            # Parse the individual product page source with BeautifulSoup
            product_soup = BeautifulSoup(product_page_source, 'html.parser')

            # Extract other product information
            # Product Details
            product_details_element = product_soup.find('div', class_='pdp-product-description-content')
            if product_details_element:
                product_data.append(product_details_element.text.strip())

            # Material and Care
            material_care_element = product_soup.find('p', class_='pdp-product-description-content')
            if material_care_element:
                product_data.append(material_care_element.text.strip())

            # Specifications
            specifications_element = product_soup.find('div', class_='index-tableContainer')
            if specifications_element:
                for row in specifications_element.find_all('div', class_='index-row'):
                    key = row.find('div', class_='index-rowKey').text.strip()
                    value = row.find('div', class_='index-rowValue').text.strip()
                    product_data.append(f"{key}: {value}")

            # Save the data to the CSV file
            writer.writerow(product_data)

            # Go back to the main page to visit the next product page
            driver.back()

# Close the browser
driver.quit()
