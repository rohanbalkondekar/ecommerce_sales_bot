import json

# Load input JSON
with open('./myntra_products_men.json') as f:
  data = json.load(f)

# Create a dict to store unique ids
unique_ids = {} 

# List to store output objects
output = []

# Loop through each object 
for obj in data:

  # Extract id
  id = obj['id']
  
  # If id already exists, skip 
  if id in unique_ids:
    continue

  # Add id to unique set
  unique_ids[id] = True

  # Append to output list
  output.append(obj) 

# Reset serial numbers
for i, obj in enumerate(output):
  obj['serial_number'] = i+1

# Write output JSON
with open('output.json', 'w') as f:
  json.dump(output, f, indent=2)