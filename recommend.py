import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load scraped assessments
df = pd.read_csv("shl_assessments.csv")

# Create a new column for combining useful text fields
df["text_blob"] = df["Assessment Name"] + " " + df["Test Type"].fillna("") + " " + df["Duration"].fillna("")

# TF-IDF vectorizer for matching queries
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["text_blob"])

def recommend_assessments(query, top_n=10):
    query_vec = vectorizer.transform([query])
    similarity_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
    top_indices = similarity_scores.argsort()[::-1][:top_n]
    results = df.loc[top_indices].copy()
    results["Score"] = similarity_scores[top_indices].round(2)

    return results[[
        "Assessment Name", "URL", "Remote Testing Support",
        "Adaptive/IRT Support", "Duration", "Test Type", "Score"
    ]]
if __name__ == "__main__":
    query = "Looking for Python and SQL test under 60 mins"
    recommendations = recommend_assessments(query)
    print(recommendations)
