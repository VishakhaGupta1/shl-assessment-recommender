import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")

# Title and description
st.title("🧠 SHL Assessment Recommender")
st.markdown("Use the tool to search assessments or get AI-based recommendations based on job descriptions.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/shl_assessments.csv")
    df.fillna("Unknown", inplace=True)
    df["combined_text"] = df["Assessment Name"] + " " + df["Test Type"] + " " + df["Duration"].astype(str)
    return df

df = load_data()

# Tabs: Manual Search | Smart Recommendations
tab1, tab2 = st.tabs(["🔎 Manual Search", "🤖 Smart Recommendations"])

# --- Tab 1: Manual Search ---
with tab1:
    search_input = st.text_input("Search by Assessment Name, Type, or Duration:")
    
    if search_input:
        filtered_df = df[df["combined_text"].str.lower().str.contains(search_input.lower())]
        st.write(f"Showing results for: **{search_input}**")
    else:
        filtered_df = df.copy()

    st.dataframe(filtered_df.drop(columns=["combined_text"]), use_container_width=True)

    # Download button
    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(filtered_df.drop(columns=["combined_text"]))
    st.download_button("📥 Download Filtered CSV", csv, "filtered_shl_assessments.csv", "text/csv")

# --- Tab 2: Smart Recommendations ---
with tab2:
    job_desc = st.text_area("Paste Job Description or Role (e.g. 'Looking for a data analyst with Excel, Python, stats...')")

    if st.button("Get Recommendations") and job_desc:
        # TF-IDF
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(df["combined_text"])
        job_vec = vectorizer.transform([job_desc])

        cosine_sim = cosine_similarity(job_vec, tfidf_matrix).flatten()
        df["Score"] = cosine_sim

        top_n = df.sort_values(by="Score", ascending=False).head(10)

        for i, row in top_n.iterrows():
            st.markdown(f"""
            ### 🔹 {row['Assessment Name']}
            **URL:** [{row['URL']}]({row['URL']})  
            **Type:** {row['Test Type']}  
            **Duration:** {row['Duration']}  
            **Remote Testing Support:** {row['Remote Testing Support']}  
            **IRT Support:** {row['Adaptive/IRT Support']}  
            **Score:** `{round(row['Score'], 4)}`
            ---
            """)
