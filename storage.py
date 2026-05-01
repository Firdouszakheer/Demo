import faiss
import pickle
import os

def save_index(index, chunks, path="vector_store"):
    os.makedirs(path, exist_ok=True)
    faiss.write_index(index, f"{path}/index.faiss")
    
    with open(f"{path}/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

def load_index(path="vector_store"):
    if not os.path.exists(path):
        return None, None
    
    index = faiss.read_index(f"{path}/index.faiss")
    
    with open(f"{path}/chunks.pkl", "rb") as f:
        chunks = pickle.load(f)
    
    return index, chunks