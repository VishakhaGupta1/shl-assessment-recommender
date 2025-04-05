import streamlit as st
import requests

st.set_page_config(page_title="SHL Assessment Recommender")

st.title("🔍 SHL Assessment Recommender")
st.write("Enter a short job description or hiring goal to get recommended SHL assessments.")

# Input text box
query = st.text_area("📝 Job Description", height=200)

if st.button("Get Recommendations"):
    if not query.strip():
        st.warning("Please enter a job description.")
    else:
        # Call your FastAPI endpoint
        try:
            response = requests.post(
                "http://127.0.0.1:8000/recommend",
                json={"query": query}
            )
            if response.status_code == 200:
                results = response.json()["results"]
                if not results:
                    st.info("No recommendations found.")
                else:
                    st.success("✅ Recommendations:")
                    for res in results:
                        st.markdown(f"### [{res['Assessment Name']}]({res['URL']})")
                        st.markdown(f"**Test Type:** {res['Test Type']}  \n"
                                    f"**Remote:** {res['Remote Testing Support']}  \n"
                                    f"**Adaptive:** {res['Adaptive/IRT Support']}  \n"
                                    f"**Score:** {res['Score']}")
                        st.markdown("---")
            else:
                st.error("API returned an error.")
        except Exception as e:
            st.error(f"⚠️ Could not connect to API: {e}")
