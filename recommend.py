import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch

# Load the Sentence-BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

def load_data():
    df = pd.read_csv('shl_assessments.csv')
    df.columns = df.columns.str.strip()  # Clean column names

    # ✅ Replace 'Description' with 'Test Type' since that's available
    df['combined_text'] = df['Assessment Name'] + " " + df['Test Type']
    return df

# Load and encode data
df = load_data()
corpus = df['combined_text'].tolist()
corpus_embeddings = model.encode(corpus, convert_to_tensor=True)

def get_recommendations(user_input, top_k=10):
    query_embedding = model.encode(user_input, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cosine_scores, k=top_k)

    results = []
    for score, idx in zip(top_results[0], top_results[1]):
        row = df.iloc[idx.item()]
        results.append({
            'Assessment Name': row['Assessment Name'],
            'URL': row['URL'],
            'Remote Testing Support': row['Remote Testing Support'],
            'IRT Support': row['Adaptive/IRT Support'],
            'Duration': row['Duration'],
            'Type': row['Test Type'],
            'Score': float(score)
        })

    return results

if __name__ == "__main__":
    query = "Hiring a frontend developer who knows React and has good problem-solving skills. Test should be under 45 minutes."
    recommendations = get_recommendations(query)

    for i, rec in enumerate(recommendations):
        print(f"\n🔹 Recommendation {i+1}")
        print(f"Name: {rec['Assessment Name']}")
        print(f"URL: {rec['URL']}")
        print(f"Remote Testing Support: {rec['Remote Testing Support']}")
        print(f"IRT Support: {rec['IRT Support']}")
        print(f"Duration: {rec['Duration']}")
        print(f"Type: {rec['Type']}")
        print(f"Score: {rec['Score']:.4f}")
