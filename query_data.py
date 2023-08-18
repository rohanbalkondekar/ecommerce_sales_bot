# import os
# import faiss
# import pickle
# from sentence_transformers import SentenceTransformer

# # Retrieve the stored list
# directory = "./ingested_data/list"
# file_path = os.path.join(directory, "list.pkl")

# if os.path.exists(file_path):
#     with open(file_path, "rb") as file:
#         stored_list = pickle.load(file)
# else:
#     print("List file does not exist.")
# data = stored_list

# def semantic_search(str):
#     model = SentenceTransformer('all-MiniLM-L6-v2')
#     index = faiss.read_index('./ingested_data/index/index')

#     query_vector = model.encode([str])
#     k = 5
#     top_k = index.search(query_vector, k)
#     # print("top K: ", top_k)
#     results = [data[_id] for _id in top_k[1].tolist()[0]]
#     return "\n\n".join(results)

# search_input = ""
# while search_input != "q":
#     search_input = input("what looking for today:   ")
#     result = semantic_search(search_input)
#     print(result)







import os
import faiss
import pickle
import json
from sentence_transformers import SentenceTransformer

# Retrieve data from the JSON file
json_file_path = "./myntra_all.json"

if os.path.exists(json_file_path):
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)
else:
    print("JSON file does not exist.")
    data = []

def semantic_search(query_str):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    index = faiss.read_index('./ingested_data/index/index')

    query_vector = model.encode([query_str])
    k = 5
    top_k = index.search(query_vector, k)
    
    result_objects = [data[_id] for _id in top_k[1].tolist()[0]]
    return "\n\n".join([json.dumps(obj, indent=4) for obj in result_objects])


search_input = ""
while search_input != "q":
    search_input = input("What are you looking for today: ")
    result = semantic_search(search_input)
    print(result)
