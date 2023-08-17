# import csv
# import json

# csv_file = './myntra.csv'
# json_file = 'converted_data.json'

# data = []

# # Read CSV and convert to list of dictionaries
# with open(csv_file, 'r', encoding='utf-8') as file:
#     csv_reader = csv.DictReader(file)
#     for row in csv_reader:
#         data.append(row)

# # Write data to JSON file
# with open(json_file, 'w', encoding='utf-8') as file:
#     json.dump(data, file, indent=2)

# print(f"CSV data converted and saved to {json_file}.")


# import csv
# import json

# csv_file = './myntra.csv'
# json_file = 'converted_data_small.json'
# top_products_count = 200

# data = []

# # Read CSV and convert to list of dictionaries
# with open(csv_file, 'r', encoding='utf-8') as file:
#     csv_reader = csv.DictReader(file)
#     for row in csv_reader:
#         # Remove "uniq_id" and "crawl_timestamp" fields
#         row.pop("uniq_id", None)
#         row.pop("crawl_timestamp", None)
#         data.append(row)
#         # Limit the data to top 200 products
#         if len(data) >= top_products_count:
#             break

# # Write data to JSON file
# with open(json_file, 'w', encoding='utf-8') as file:
#     json.dump(data, file, indent=2)

# print(f"CSV data converted and top {top_products_count} products saved to {json_file}.")



import csv

def clean_csv(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        cleaned_data = []
        
        for row in reader:
            # Remove extra fields if there are more than 25 fields in a row
            if len(row) > 25:
                cleaned_row = row[:25]
            else:
                cleaned_row = row
            
            cleaned_data.append(cleaned_row)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(cleaned_data)

if __name__ == "__main__":
    input_csv_file = "myntra.csv"
    output_csv_file = "cleaned_myntra.csv"
    
    clean_csv(input_csv_file, output_csv_file)
    print(f"CSV file cleaned and saved as '{output_csv_file}'.")
