import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("shl_assessments.csv")

# Convert 'Duration' to numeric, handling 'Unknown' as NaN
df["Duration_Mins"] = pd.to_numeric(df["Duration"], errors="coerce")

# Sidebar filters
st.sidebar.title("Filter Assessments")

remote_filter = st.sidebar.selectbox("Remote Testing Support", ["All", "Yes", "No"])
adaptive_filter = st.sidebar.selectbox("Adaptive/IRT Support", ["All", "Yes", "No"])
duration_filter = st.sidebar.slider("Max Duration (minutes)", 0, 120, 60)
search_filter = st.sidebar.text_input("Search by Assessment Name")

# Apply filters
filtered_df = df.copy()

if remote_filter != "All":
    filtered_df = filtered_df[filtered_df["Remote Testing Support"] == remote_filter]

if adaptive_filter != "All":
    filtered_df = filtered_df[filtered_df["Adaptive/IRT Support"] == adaptive_filter]

# Filter on duration: show assessments with unknown duration or within limit
filtered_df = filtered_df[
    (filtered_df["Duration_Mins"].isna()) | (filtered_df["Duration_Mins"] <= duration_filter)
]

if search_filter:
    filtered_df = filtered_df[
        filtered_df["Assessment Name"].str.contains(search_filter, case=False, na=False)
    ]

# Replace Duration_Mins with "Unknown" or int
filtered_df["Duration"] = filtered_df["Duration_Mins"].apply(
    lambda x: "Unknown" if pd.isna(x) else int(x)
)

# Drop Duration_Mins (optional, cleaner display)
filtered_df = filtered_df.drop(columns=["Duration_Mins"])

# Title
st.markdown("## 🔍 SHL Assessment Explorer")
st.write(f"### Showing {len(filtered_df)} assessments")

# Show filtered table
st.dataframe(filtered_df.reset_index(drop=True))

# Download filtered data
st.download_button(
    "📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_shl_assessments.csv",
    mime="text/csv"
)
