import os
import faiss
from sentence_transformers import SentenceTransformer

images_folder = 'images'
image_files = [os.path.join(images_folder, f) for f in os.listdir(images_folder)]

index = faiss.read_index('image_index.faiss')
model = SentenceTransformer('clip-ViT-B-32')

text_query = "white shirt"
query_embedding = model.encode(text_query)
query_embedding = query_embedding.reshape(1, -1)

k = 5
print("Searching for similar images...")
top_k = index.search(query_embedding, k)

print("Top {} similar images:".format(k))
for id, score in zip(top_k[1][0], top_k[0][0]):
    print("- Image {} (Score: {})".format(image_files[id], score))