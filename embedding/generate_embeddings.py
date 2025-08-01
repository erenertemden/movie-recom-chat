import pandas as pd
import numpy as np
import faiss
import sys
import requests
import time
import os
from textual_rep import create_textual_rep
from embedding.utils.ollama_check import check_ollama_alive

# Ollama kontrolü
if not check_ollama_alive():
    sys.exit("Ollama başlatılmadan işlem yapılamaz.")

# Veri yükle
df = pd.read_csv("embedding/data/netflix_titles.csv")
df['textual_rep'] = df.apply(create_textual_rep, axis=1)

# Örnek bir embedding alarak boyutu belirle
print("Embedding boyutu belirleniyor...")
sample_text = df["textual_rep"].iloc[0]
res = requests.post("http://localhost:11434/api/embeddings", json={
    "model": "phi3:mini",
    "prompt": sample_text
})
if res.status_code != 200:
    sys.exit(f"Hata: Embedding alınamadı. Yanıt: {res.text}")

embedding = np.array(res.json()["embedding"]).astype("float32")
dim = embedding.shape[0]
print(f"Embedding boyutu: {dim}")

# Embedding dizisi oluştur
X = np.zeros((len(df), dim), dtype="float32")
X[0] = embedding  # İlk satır işlenmiş oldu

# Embedding döngüsü
for i in range(1, len(df)):
    try:
        text = df["textual_rep"].iloc[i]

        if i % 100 == 0:
            print(f"{i}/{len(df)} satır işlendi.")
            time.sleep(5)

        res = requests.post("http://localhost:11434/api/embeddings", json={
            "model": "phi3:mini",
            "prompt": text
        })

        embedding = np.array(res.json()["embedding"]).astype("float32")

        if embedding.shape[0] != dim:
            print(f"Hata {i}. satırda: Beklenen {dim}, gelen {embedding.shape[0]}")
            continue

        X[i] = embedding

        # Her 500 satırda bir kaydet
        if i % 500 == 0:
            np.save("embedding/data/embeddings_partial.npy", X)
            print("Ara kayıt yapıldı (embeddings_partial.npy)")

    except Exception as e:
        print(f"Hata {i}. satırda: {e}")
        continue

# Kaydet
np.save("embedding/data/embeddings.npy", X)
index = faiss.IndexFlatL2(dim)
index.add(X)
faiss.write_index(index, "embedding/data/index.faiss")

print("Embedding ve FAISS index oluşturuldu.")
