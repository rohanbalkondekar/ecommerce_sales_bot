import os
import faiss 
import numpy as np
from sentence_transformers import SentenceTransformer

images_folder = 'images'
image_files = [os.path.join(images_folder, f) for f in os.listdir(images_folder)] 
print(image_files)

model = SentenceTransformer('clip-ViT-B-32')

print("Encoding images...")
image_embeddings = model.encode(image_files)

index = faiss.IndexIDMap(faiss.IndexFlatIP(image_embeddings.shape[1]))
index.add_with_ids(image_embeddings, np.array(range(len(image_files))))

faiss.write_index(index, 'image_index.faiss') 
print("{} images encoded and indexed.".format(len(image_files)))