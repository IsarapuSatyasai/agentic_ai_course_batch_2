from openai import OpenAI
from dotenv import load_dotenv
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
client = OpenAI()

def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small",
    )
    return response.data[0].embedding

def similarity(a, b):
    return cosine_similarity([a], [b])[0][0]

# 1. What is a Vector Embedding?
print("1. What is a Vector Embedding?")
cat = get_embedding("cat")
print("Length :", len(cat))
print("First 8 numbers: ", [round(x, 4) for x in cat[:8]])

# 2. Similar things live close
print("2. Similarity")
dog = get_embedding("dog")
car = get_embedding("car")

print("cat <-> dog :", round(similarity(cat, dog), 4))
print("cat <-> car :", round(similarity(cat, car), 4))

# 3. Famouse math: King - Man + Woman = Queen
print("Famous math: King - Man + Woman = Queen")
king = np.array(get_embedding("king"))
man = np.array(get_embedding("man"))
woman = np.array(get_embedding("woman"))
queen = king - man + woman

print("king <-> queen :", round(similarity(king, queen), 4))