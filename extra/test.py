from selenium import webdriver

# Create a new instance of the Firefox WebDriver
driver = webdriver.Firefox()

# URL of the Myntra men topwear page
url = 'https://www.myntra.com/men-topwear'

# Open the URL in the browser
driver.get(url)

# Get and print the title of the page
print("Page Title:", driver.title)

# Close the browser
driver.quit()
