import json
from selenium import webdriver
from bs4 import BeautifulSoup

# Create webdriver instance
driver = webdriver.Firefox() 

# Global list to store all scraped data
all_products = []


def scrape_product(product_link):

  global all_products
  global serial_number

  try:
    # Navigate to product page
    driver.get(product_link)

    # Parse page source
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Get product id from url
    product_id = product_link.split('/')[-2]

    # Scrape Product Details
    product_brand = soup.find('h1', class_='pdp-title').text.strip() if soup.find('h1', class_='pdp-title') else None
    product_name = soup.find('h1', class_='pdp-name').text.strip() if soup.find('h1', class_='pdp-name') else None
    product_desc = soup.find('p', class_='pdp-product-description-content').text.strip() if soup.find('p', class_='pdp-product-description-content') else None
    product_price = soup.find('span', class_='pdp-price').text.strip() if soup.find('span', class_='pdp-price') else None
    product_rating = soup.find('div', class_='index-overallRating').text.strip() if soup.find('div', class_='index-overallRating') else None


    specs = {}
    if soup.find('div', class_='index-tableContainer'):
        specs_table = soup.find('div', class_='index-tableContainer').find_all('div', class_='index-row')
        for row in specs_table:
            key = row.find('div', class_='index-rowKey').text.strip()
            value = row.find('div', class_='index-rowValue').text.strip() 
            specs[key] = value

    sizes = [size.find('p', class_='size-buttons-unified-size').text.strip() for size in soup.find_all('div', class_='size-buttons-tipAndBtnContainer') if size.find('p', class_='size-buttons-unified-size')]

  ##
    offers = []
    for offer in soup.find_all('div', class_='pdp-offers-offer'):
      title = offer.find('div', class_='pdp-offers-offerTitle').text.strip()
      details = [li.text.strip() for li in offer.find_all('li')]
      offer = {
          'title': title,
          'details': details  
      }
      offers.append(offer)

    ##

    # Create product dict 
    product = {
        'id': product_id,
        'brand': product_brand,
        'name': product_name,
        'link': product_link,
        'description': product_desc,
        'price': product_price,
        'rating': product_rating,
        'specs': specs,
        'sizes': sizes,
        'offers': offers
    }

    # Print product scraped
    print(f"Scraped Product: {product_id}")

    # Append product to global list
    all_products.append(product)

    # Update JSON file after each product 
    with open('temp_myntra_products.json', 'w') as f:
        json.dump(all_products, f, indent=4)

  except Exception as e:
    print(f"Error scraping {product_link} - {e}")

def main():

  # Navigate to listing page
  # driver.get('https://www.myntra.com/men-topwear')
  driver.get('https://www.myntra.com/toys?p=2')


  # Parse page 
  soup = BeautifulSoup(driver.page_source, 'html.parser')

  # Find all products
  products = soup.find_all('li', class_='product-base')

  for product in products:
    link = "https://www.myntra.com/" + product.find('a', href=True)['href']
    scrape_product(link)

  driver.quit()

if __name__ == "__main__":
  main()