import json
import time
from selenium import webdriver
from bs4 import BeautifulSoup

def main():
    # Create a webdriver instance
    driver = webdriver.Firefox()

    # Initialize the output data list
    output_data = []

    try:
        # Navigate to the listing page
        driver.get('http://demo.miindkraft.com/web/review360.php')

        for emp_id_num in range(1, 301):
            emp_id = f'IAE{emp_id_num}'

            # Find the input field, enter the employee ID, and click the search button
            input_element = driver.find_element('css selector', 'input[name="emp_id"]')
            input_element.clear()
            input_element.send_keys(emp_id)

            search_button = driver.find_element('id', 'get_data')
            search_button.click()

            # Wait for the table to load
            time.sleep(2)

            # Parse the page source
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract employee data
            emp_name = soup.find('b', id='LastName').text.strip()
            reviews = []
            table_rows = soup.select('#userTable tr')
            for row in table_rows[1:]:
                columns = row.find_all('td')
                review_name = columns[1].text.strip()
                review_id = columns[2].text.strip()
                review_status = "completed" if columns[4].find('button', {'class': 'buttonNext'})['style'] == "background-color: gray;" else "pending"
                reviews.append({
                    "Name": review_name,
                    "ID": review_id,
                    "Status": review_status
                })

            # Append data to output list
            output_data.append({
                "Employee_ID": emp_id,
                "Employee_name": emp_name,
                "Reviews": reviews
            })

            # Print progress
            print(f"Processed: {emp_id}")

    finally:
        # Quit the webdriver
        driver.quit()

    # Write output data to a JSON file
    with open('employee_reviews.json', 'w') as json_file:
        json.dump(output_data, json_file, indent=2)

if __name__ == "__main__":
    main()
