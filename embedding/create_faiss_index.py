import faiss
import numpy as np

X = np.load("data/embeddings.npy").astype("float32")
index = faiss.IndexFlatL2(X.shape[1])  # L2 mesafeli temel FAISS index
index.add(X)
faiss.write_index(index, "data/index.faiss")

print("FAISS indexed!")
