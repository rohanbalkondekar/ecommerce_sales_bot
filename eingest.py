import os
import json
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
# embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")

ingested_data_directory = "./ingested_data"
if not os.path.exists(ingested_data_directory):
    os.makedirs(ingested_data_directory)

# list to store to retrive later
def save_list(list):
    directory = "./ingested_data/list"
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, "list.pkl")
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            existing_list = pickle.load(file)
        existing_list.extend(list)
        with open(file_path, "wb") as file:
            pickle.dump(existing_list, file)
    else:
        with open(file_path, "wb") as file:
            pickle.dump(list, file)


def json_to_string(path):
    with open(path) as f:
        data = json.load(f)
    product_strings = []
    for product in data:
        brand = product['brand']
        name = product['name']
        description = product['description']

        string = f"Brand: {brand}, Name: {name}, Description: {description}"
        
        product_strings.append(string)

    return product_strings

def ingest(json_file):
    data_list = json_to_string(json_file)
    save_list(data_list)

    encoded_data = model.encode(data_list)
    index = faiss.IndexIDMap(faiss.IndexFlatIP(384))
    index.add_with_ids(encoded_data, np.array(range(0, len(data_list))))

    # --------- Saving as FAISS index
    directory = "./ingested_data/index"
    if not os.path.exists(directory):
        os.makedirs(directory)
    faiss.write_index(index, './ingested_data/index/index')


json_file_path = "./myntra_all.json"
ingest(json_file_path)