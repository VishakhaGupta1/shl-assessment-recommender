# SHL Assessment Recommender System

A personalized SHL test recommender system that helps users explore and get suggestions for SHL assessments based on their interests and background.

---

## 🔍 Project Overview

This project provides:
- Web Scraping to extract SHL assessment data
- TF-IDF-based Recommendation System to suggest similar assessments
- FastAPI Backend for recommendation APIs
- Streamlit Frontend for interactive exploration

---

## 📁 Folder Structure

shl-assessment-recommender/
├── app.py              # Streamlit frontend app
├── api.py              # FastAPI backend server
├── recommend.py        # Recommendation logic using TF-IDF
├── scrape_shl.py       # Script to scrape SHL assessments
│
├── data/
│   └── assessments.csv  # Cleaned SHL data
│
├── notebooks/
│   └── exploration.ipynb  # EDA and model testing
│
├── utils/
│   └── helpers.py       # Shared utility functions (if any)
│
├── requirements.txt     # Python dependencies
└── README.md            # You're here!

---

## 🚀 How to Run

1. **Install packages**
   ```bash
   pip install -r requirements.txt


Run backend

uvicorn api:app --reload


Run frontend

streamlit run app.py


📌 Technologies Used
FastAPI, Streamlit, sklearn, pandas, BeautifulSoup, TF-IDF

