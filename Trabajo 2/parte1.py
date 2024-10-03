import pandas as pd
import nltk
from nltk.tokenize import TweetTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD

# CARGA DEL CSV
print("Cargando los datos desde el archivo CSV...")
df = pd.read_csv('climateTwitterData.csv')

# Visualizar las primeras 3 filas
print("\nPrimeras 3 filas del DataFrame original:")
print(df.head(3).to_string(index=False))  # Imprime sin índice para mejor legibilidad

# TOKENIZACIÓN
print("\nDescargando el paquete de tokenización de NLTK 'punkt'...")
nltk.download('punkt')

print("\nTokenizando los textos usando TweetTokenizer...")
texts = df['text'].tolist()
tokenized_tweets = [TweetTokenizer().tokenize(text) for text in texts]
df['tokenized_text'] = tokenized_tweets

# Mostrar los primeros 3 textos originales junto con su versión tokenizada
print("\nPrimeras 3 filas con texto original y texto tokenizado:")
print(df[['text', 'tokenized_text']].head(3).to_string(index=False))

# CREACIÓN DEL BOW (BAG OF WORDS)
print("\nCreando la matriz BoW a partir de la columna 'text'...")
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['text'])

# Mostrar las primeras 5 filas de la matriz BoW en su formato disperso
print("\nPrimeras 5 filas de la matriz BoW (formato disperso):")
print(X[:5])

# REDUCCIÓN DE DIMENSIONALIDAD
print("\nAplicando reducción de dimensionalidad con TruncatedSVD (n_components=2)...")
svd = TruncatedSVD(n_components=2)
X_reduced = svd.fit_transform(X)

# Mostrar la matriz reducida
print("\nMatriz reducida a 2 dimensiones:")
print(X_reduced[:5])  # Muestra las primeras 5 filas de la matriz reducida
