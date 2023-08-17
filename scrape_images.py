# from selenium import webdriver
# from bs4 import BeautifulSoup
# import requests
# import os

# driver = webdriver.Firefox()
# driver.get('https://www.myntra.com/men-topwear')

# page_content = driver.page_source
# soup = BeautifulSoup(page_content, 'html.parser')

# # Create folders 
# os.makedirs('thumbnails', exist_ok=True)

# for product in soup.find_all('li', class_='product-base'):

#   img_tag = product.find('img')
#   if img_tag:
#     img_url = img_tag['src']
#     product_id = img_url.split('/')[-1].split('.')[0]

#     # Download image
#     img_data = requests.get(img_url).content  

#     # Save image 
#     image_path = os.path.join('thumbnails', f"{product_id}.jpg")
#     with open(image_path, 'wb') as f:
#       f.write(img_data)

#     print(f"Downloaded image: {image_path}")
      
# driver.quit()







from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import os

driver = webdriver.Firefox()
driver.get('https://www.myntra.com/men-topwear') 

os.makedirs('images', exist_ok=True)

while True:

  soup = BeautifulSoup(driver.page_source, 'html.parser')

  for product in soup.find_all('li', class_='product-base'):

    img_tag = product.find('img')
    if img_tag:
      img_url = img_tag['src']
      product_id = img_url.split('/')[-1].split('.')[0]

      # Download image
      img_data = requests.get(img_url).content

      # Save with product ID 
      image_path = os.path.join('images', f"{product_id}.jpg")  
      with open(image_path, 'wb') as f:
        f.write(img_data)

      print(f"Downloaded {image_path}")

  # Click next page button
  next_button = driver.find_element_by_class_name('pagination-next')
  if next_button.is_enabled():
    next_button.click()
  else:
    break

driver.quit()