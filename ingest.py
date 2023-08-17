import os
import json
import faiss
import pickle
import numpy as np
import pandas as pd
from PIL import Image
from docx import Document
from bs4 import BeautifulSoup
from langchain.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

folder_path = './data'
model = SentenceTransformer('all-MiniLM-L6-v2')
# embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")

ingested_data_directory = "./ingested_data"
if not os.path.exists(ingested_data_directory):
    os.makedirs(ingested_data_directory)



def read_json_objects(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        json_objects = [json.dumps(obj) for obj in data]
        return json_objects

def ingestText(text):

    json_file_path = "./Data/converted_data_small.json"
    data_list = read_json_objects(json_file_path)


    # list to store to retrive later
    new_list = data_list
    directory = "./ingested_data/list"
    if not os.path.exists(directory):
        os.makedirs(directory)
    # File path for storing the list
    file_path = os.path.join(directory, "list.pkl")
    if os.path.exists(file_path):
        # Load the existing list from the pickle file
        with open(file_path, "rb") as file:
            existing_list = pickle.load(file)
    # Extend the existing list with the new list
        existing_list.extend(new_list)
    # Store the extended list as a pickle file
        with open(file_path, "wb") as file:
            pickle.dump(existing_list, file)
    else:
        # Store the new list as a pickle file
        with open(file_path, "wb") as file:
            pickle.dump(new_list, file)


    encoded_data = model.encode(data_list)
    index = faiss.IndexIDMap(faiss.IndexFlatIP(384))
    index.add_with_ids(encoded_data, np.array(range(0, len(data_list))))
    # vectorstore = FAISS.from_texts(texts=data, embedding=embeddings)

    # --------- Saving as FAISS index
    directory = "./ingested_data/index"
    if not os.path.exists(directory):
        os.makedirs(directory)

    faiss.write_index(index, './ingested_data/index/index')


# ─── For Text Files ───────────────────────────────────────────────────────────
def ingestJSON(folder_path):
    def read_txt_files(folder_path):
        file_list = os.listdir(folder_path)
        text = ""
        for file_name in file_list:
            if file_name.endswith('.json'):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, "r", encoding="utf-8") as file:
                    file_text = file.read()
                    text += file_text + "\n"
        return text

    text = read_txt_files(folder_path)

    ingestText(text)


ingestJSON(folder_path)