import json
from selenium import webdriver
from bs4 import BeautifulSoup
import os

driver = webdriver.Firefox()

def scrape_product_details(product_link):
    try:
        driver.get(product_link)
        product_page_source = driver.page_source
        product_soup = BeautifulSoup(product_page_source, 'html.parser')

        product_brand_element = product_soup.find('h3', class_='product-brand')
        product_brand = product_brand_element.text.strip() if product_brand_element else None

        product_name_element = product_soup.find('h4', class_='product-product')
        product_name = product_name_element.text.strip() if product_name_element else None

        product_desc_element = product_soup.find('p', class_='pdp-product-description-content')
        product_desc = product_desc_element.text.strip() if product_desc_element else None

        product_price_element = product_soup.find('span', class_='pdp-price')
        product_price = product_price_element.text.strip() if product_price_element else None

        product_rating_element = product_soup.find('div', class_='index-overallRating')
        product_rating = product_rating_element.text.strip() if product_rating_element else None

        product_specifications_element = product_soup.find('div', class_='index-tableContainer')
        specs_dict = {}
        if product_specifications_element:
            product_specifications = product_specifications_element.find_all('div', class_='index-row')
            for spec in product_specifications:
                key = spec.find('div', class_='index-rowKey').text.strip()
                value = spec.find('div', class_='index-rowValue').text.strip()
                specs_dict[key] = value

        product_sizes = product_soup.find_all('div', class_='size-buttons-tipAndBtnContainer')
        sizes = [sz.find('p', class_='size-buttons-unified-size').text.strip() for sz in product_sizes if sz.find('p', class_='size-buttons-unified-size')]

        product_data = {
            'Product Brand': product_brand,
            'Product Name': product_name,
            'Product Link': product_link,
            'Product Description': product_desc,
            'Product Price': product_price,
            'Product Rating': product_rating,
            'Product Specifications': specs_dict,
            'Sizes': sizes
        }
        return product_data
    except Exception as e:
        print(f"Error occurred while scraping product: {product_link}")
        print(f"Error details: {str(e)}")
        return None

def main():
    driver = webdriver.Firefox()
    url = 'https://www.myntra.com/men-topwear'
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    product_list = soup.find_all('li', class_='product-base')

    scraped_products = []
    for product in product_list:
        product_link_element = product.find('a', href=True)
        if product_link_element:
            product_link = "https://www.myntra.com/" + product_link_element['href']
            product_data = scrape_product_details(product_link)
            if product_data:
                scraped_products.append(product_data)
                product_file_path = f"product_{product_link.split('/')[-2]}.json"

                # If the JSON file for the product exists, update it; otherwise, create a new one.
                if os.path.exists(product_file_path):
                    with open(product_file_path, 'r', encoding='utf-8') as json_file:
                        existing_data = json.load(json_file)
                    existing_data.update(product_data)

                    with open(product_file_path, 'w', encoding='utf-8') as json_file:
                        json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
                else:
                    with open(product_file_path, 'w', encoding='utf-8') as json_file:
                        json.dump(product_data, json_file, ensure_ascii=False, indent=4)

                print(f"Product details saved for: {product_data['Product Name']}")

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    main()
import json
from selenium import webdriver
from bs4 import BeautifulSoup
import os

driver = webdriver.Firefox()

def scrape_product_details(product_link):
    try:
        driver.get(product_link)
        product_page_source = driver.page_source
        product_soup = BeautifulSoup(product_page_source, 'html.parser')

        product_brand_element = product_soup.find('h3', class_='product-brand')
        product_brand = product_brand_element.text.strip() if product_brand_element else None

        product_name_element = product_soup.find('h4', class_='product-product')
        product_name = product_name_element.text.strip() if product_name_element else None

        product_desc_element = product_soup.find('p', class_='pdp-product-description-content')
        product_desc = product_desc_element.text.strip() if product_desc_element else None

        product_price_element = product_soup.find('span', class_='pdp-price')
        product_price = product_price_element.text.strip() if product_price_element else None

        product_rating_element = product_soup.find('div', class_='index-overallRating')
        product_rating = product_rating_element.text.strip() if product_rating_element else None

        product_specifications_element = product_soup.find('div', class_='index-tableContainer')
        specs_dict = {}
        if product_specifications_element:
            product_specifications = product_specifications_element.find_all('div', class_='index-row')
            for spec in product_specifications:
                key = spec.find('div', class_='index-rowKey').text.strip()
                value = spec.find('div', class_='index-rowValue').text.strip()
                specs_dict[key] = value

        product_sizes = product_soup.find_all('div', class_='size-buttons-tipAndBtnContainer')
        sizes = [sz.find('p', class_='size-buttons-unified-size').text.strip() for sz in product_sizes if sz.find('p', class_='size-buttons-unified-size')]

        product_data = {
            'Product Brand': product_brand,
            'Product Name': product_name,
            'Product Link': product_link,
            'Product Description': product_desc,
            'Product Price': product_price,
            'Product Rating': product_rating,
            'Product Specifications': specs_dict,
            'Sizes': sizes
        }
        return product_data
    except Exception as e:
        print(f"Error occurred while scraping product: {product_link}")
        print(f"Error details: {str(e)}")
        return None

def main():
    driver = webdriver.Firefox()
    url = 'https://www.myntra.com/men-topwear'
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    product_list = soup.find_all('li', class_='product-base')

    scraped_products = []
    for product in product_list:
        product_link_element = product.find('a', href=True)
        if product_link_element:
            product_link = "https://www.myntra.com/" + product_link_element['href']
            product_data = scrape_product_details(product_link)
            if product_data:
                scraped_products.append(product_data)
                product_file_path = f"product_{product_link.split('/')[-2]}.json"

                # If the JSON file for the product exists, update it; otherwise, create a new one.
                if os.path.exists(product_file_path):
                    with open(product_file_path, 'r', encoding='utf-8') as json_file:
                        existing_data = json.load(json_file)
                    existing_data.update(product_data)

                    with open(product_file_path, 'w', encoding='utf-8') as json_file:
                        json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
                else:
                    with open(product_file_path, 'w', encoding='utf-8') as json_file:
                        json.dump(product_data, json_file, ensure_ascii=False, indent=4)

                print(f"Product details saved for: {product_data['Product Name']}")

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    main()
