import os
import openai
import numpy as np
import faiss
import pandas as pd
from dotenv import load_dotenv
from embedding.textual_rep import create_textual_rep

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

EMBEDDINGS = np.load("embedding/data/embeddings.npy").astype("float32")
INDEX = faiss.read_index("embedding/data/index.faiss")
DF = pd.read_csv("embedding/data/netflix_titles.csv")
DF['textual_rep'] = DF.apply(lambda row: create_textual_rep(row), axis=1)

def embed_with_openai(text, model="text-embedding-3-large"):
    response = openai.Embedding.create(
        input=text,
        model=model
    )
    return np.array(response['data'][0]['embedding'], dtype="float32").reshape(1, -1)

def get_top_k_context(query, top_k=3):
    query_emb = embed_with_openai(query)
    D, I = INDEX.search(query_emb, top_k)
    context_texts = [DF.iloc[idx]["textual_rep"] for idx in I[0]]
    return context_texts
