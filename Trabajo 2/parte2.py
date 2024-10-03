from sentence_transformers import SentenceTransformer
import pandas as pd
import chromadb

# CARGA DEL CSV
print("Cargando los datos desde el archivo CSV...")
df = pd.read_csv('climateTwitterData.csv')

# Visualizar las primeras 3 filas
print("\nPrimeras 3 filas del DataFrame original:")
print(df.head(3).to_string(index=False))  # Imprime sin índice para mejor legibilidad

# TOKENIZACIÓN Y EMBEDDING DE LA COLUMNA TEXTS
texts = df['text'].tolist()

# Carga del modelo
print("Cargando modelo de embeddings 'all-MiniLM-L6-v2'...")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Generación de embeddings para los textos
print("Generando embeddings...")
embeddings = model.encode(texts)

# Conexión con ChromaDB 
print("Conectando a ChromaDB...")
client = chromadb.Client()

# Creación de una colección donde almacenar los embeddings
collection = client.create_collection("climate_texts_embeddings")

# Indexación y mapeo los embeddings en ChromaDB
print("Indexando los embeddings en ChromaDB...")
for idx, text in enumerate(texts):
    
    collection.add(
        documents=[text],  # Texto original
        embeddings=[embeddings[idx]],  # Embedding
        ids=[str(idx)]  # ID único
    )

print("Embeddings indexados correctamente.")

# Consulta de ejemplo
query = "What can we do to combat climate change?"  # Consulta de ejemplo
print(f"\nRealizando query: {query}")

# Embedding del query
query_embedding = model.encode([query])

# Consultar los 5 documentos más cercanos en ChromaDB al embedding del query
results = collection.query(query_embeddings=query_embedding, n_results=5)

# Mostrar los resultados
print("Textos más similares a la consulta:")
for doc, score in zip(results['documents'][0], results['distances'][0]):
    print(f"\nTexto: {doc}\nSimilitud: {score}")