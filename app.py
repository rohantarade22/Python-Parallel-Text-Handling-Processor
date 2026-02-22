import streamlit as st
import sqlite3
import pandas as pd
import time

from core.storage import create_database, insert_text
from core.text_loader import parallel_process
from core.rule_engine import score_text
from core.search_engine import search_data


# Page Configuration

st.set_page_config(page_title="Parallel Text Processor")

st.title(" Parallel Text Handling Processor")

# Initialize Database
create_database()

st.markdown("Upload a text file to process using parallel threads.")


# File Upload Section
uploaded_file = st.file_uploader("Upload Text File", type=["txt"])

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")
    st.success("File uploaded successfully ")

    if st.button("Start Processing"):

        start_time = time.time()

        # Step 1: Parallel Cleaning
        processed_chunks = parallel_process(text)

        total_processed = 0
        positive_count = 0
        negative_count = 0

        # Step 2: Sentiment Scoring + Store in DB
        for chunk in processed_chunks:
            score = score_text(chunk)

            if score > 0:
                tag = "Positive"
                positive_count += 1
            elif score < 0:
                tag = "Negative"
                negative_count += 1
            else:
                tag = "Neutral"

            insert_text(chunk, score, tag)
            total_processed += 1

        end_time = time.time()

        # Step 3: Show Summary
        st.success("Processing Completed 🎉")

        st.write("### 📊 Processing Summary")
        st.write(f"Total Chunks Processed: {total_processed}")
        st.write(f"Positive Chunks: {positive_count}")
        st.write(f"Negative Chunks: {negative_count}")
        st.write(f"Neutral Chunks: {total_processed - positive_count - negative_count}")
        st.write(f"Execution Time: {round(end_time - start_time, 2)} seconds")

        st.write("### 🔍 Sample Processed Data")
        st.write(processed_chunks[:5])


# -----------------------------
# View Database Section
# -----------------------------
st.markdown("---")
st.subheader("📂 View Stored Database Data")

if st.button("Show Stored Data"):
    conn = sqlite3.connect("database/processor.db")
    df = pd.read_sql_query("SELECT * FROM texts", conn)
    conn.close()

    st.dataframe(df)

# -----------------------------
# Search & Filter Section
# -----------------------------
st.markdown("---")
st.subheader("🔍 Search & Filter Database")

keyword = st.text_input("Enter keyword to search")

col1, col2 = st.columns(2)

with col1:
    min_score = st.text_input("Minimum Sentiment Score (optional)")

with col2:
    max_score = st.text_input("Maximum Sentiment Score (optional)")

if st.button("Search Database"):

    # Convert score inputs safely
    min_val = int(min_score) if min_score.strip() != "" else None
    max_val = int(max_score) if max_score.strip() != "" else None

    results_df = search_data(
        keyword=keyword if keyword.strip() != "" else None,
        min_score=min_val,
        max_score=max_val
    )

    st.write("### Search Results")
    st.dataframe(results_df)