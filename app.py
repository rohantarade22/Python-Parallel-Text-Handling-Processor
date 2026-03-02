import streamlit as st
import sqlite3
import pandas as pd
import time

from core.storage import create_database, insert_text
from core.text_loader import parallel_process
from core.rule_engine import score_text
from core.search_engine import search_data
import matplotlib.pyplot as plt
from core.storage import clear_database
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from core.storage import bulk_insert

# Page Configuration

st.set_page_config(page_title="Parallel Text Processor")

st.title(" Parallel Text Handling Processor")

# Initialize Database
create_database()

st.markdown("Upload a text file to process using parallel threads.")


# File Upload Section .............SECTION 1
uploaded_file = st.file_uploader("Upload Text File", type=["txt"])

if uploaded_file is not None:
    clear_option = st.checkbox("Clear previous data before processing")
    text = uploaded_file.read().decode("utf-8")
    st.success("File uploaded successfully ")

    chunk_size = st.number_input(
    "Enter chunk size (characters per chunk)",
    min_value=50,
    max_value=2000,
    value=200,
    step=50
)
    if st.button("Start Processing"):

        # Clear DB only if user selected checkbox
        if clear_option:
            clear_database()
            st.warning("Previous database records cleared.")

        st.info("Processing started...")
       
        # Split text into chunks
        from core.chunker import split_into_chunks
        chunks = split_into_chunks(text, chunk_size)

        #  Sequential Processing
        start_seq = time.time()

        seq_scores = []
        for chunk in chunks:
            seq_scores.append(score_text(chunk))

        end_seq = time.time()
        sequential_time = end_seq - start_seq

        # Threading
        start_thread = time.time()

        with ThreadPoolExecutor() as executor:
            thread_scores = list(executor.map(score_text, chunks))

        end_thread = time.time()
        thread_time = end_thread - start_thread

        # Multiprocessing
        start_process = time.time()

        with ProcessPoolExecutor() as executor:
            process_scores = list(executor.map(score_text, chunks))

        end_process = time.time()
        process_time = end_process - start_process

        # Store Only One Version in DB (Thread result)

        records_to_insert = []

        for chunk, score in zip(chunks, thread_scores):

            if score > 0:
                tag = "Positive"
            elif score < 0:
                tag = "Negative"
            else:
                tag = "Neutral"

            records_to_insert.append((chunk, score, tag))

        # Bulk insert (we will optimize more in Phase 4)
        bulk_insert(records_to_insert)

        # Display Performance

        st.success("Processing Completed 🎉")

        col1, col2, col3 = st.columns(3)

        col1.metric("Sequential Time (sec)", round(sequential_time, 4))
        col2.metric("Threading Time (sec)", round(thread_time, 4))
        col3.metric("Multiprocessing Time (sec)", round(process_time, 4))    
            
# View Database Section ...................SECTION 2
st.markdown("---")
st.subheader("📂 View Stored Database Data")

if st.button("Show Stored Data"):
    conn = sqlite3.connect("database/processor.db")
    df = pd.read_sql_query("SELECT * FROM texts", conn)
    conn.close()

    st.dataframe(df)


# Search & Filter Section........................SECTION 3

st.markdown("---")
st.subheader("🔍 Search & Filter Database")

# Input fields
keyword = st.text_input("Enter keyword to search")

col1, col2 = st.columns(2)

with col1:
    min_score = st.text_input("Minimum Sentiment Score (optional)")

with col2:
    max_score = st.text_input("Maximum Sentiment Score (optional)")

# Search Button
if st.button("Search Database"):

    # Convert text inputs to integers safely
    min_val = int(min_score) if min_score.strip() != "" else None
    max_val = int(max_score) if max_score.strip() != "" else None

    # Call search function
    results_df = search_data(
        keyword=keyword.strip() if keyword.strip() != "" else None,
        min_score=min_val,
        max_score=max_val
    )

    # Display results
    st.write("### Search Results")
    st.dataframe(results_df)

    # Store filtered data for CSV export
    st.session_state["filtered_data"] = results_df



#  Professional Sentiment Dashboard......................SECTION 4 

st.markdown("---")
st.subheader("📊 Sentiment Analytics Dashboard")

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Load Data (Filtered OR Full)

if "filtered_data" in st.session_state and not st.session_state["filtered_data"].empty:
    df = st.session_state["filtered_data"]
else:
    conn = sqlite3.connect("database/processor.db")
    df = pd.read_sql_query("SELECT * FROM texts", conn)
    conn.close()

# If Data Exists
if not df.empty:

    # Basic Metrics
    total_records = len(df)
    avg_score = df["sentiment_score"].mean()

    positive = len(df[df["sentiment_score"] > 0])
    negative = len(df[df["sentiment_score"] < 0])
    neutral = len(df[df["sentiment_score"] == 0])

    # ------------------ METRICS ROW ------------------
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Records", total_records)
    col2.metric("Average Score", round(avg_score, 2))
    col3.metric("Positive", positive)
    col4.metric("Negative", negative)
    col5.metric("Neutral", neutral)

    st.markdown("")

    # ------------------ CHARTS ROW ------------------
    chart_col1, chart_col2 = st.columns(2)

    # ------------------ Pie Chart ------------------
    with chart_col1:
        st.markdown("### Sentiment Distribution")

        fig1, ax1 = plt.subplots(figsize=(5, 3))
        ax1.pie(
            [positive, negative, neutral],
            labels=["Positive", "Negative", "Neutral"],
            autopct='%1.1f%%'
        )
        ax1.set_title("Sentiment Distribution")
        st.pyplot(fig1)

    # ------------------ Bar Chart ------------------
    with chart_col2:
        st.markdown("### Sentiment Comparison")

        fig2, ax2 = plt.subplots(figsize=(5, 5))
        ax2.bar(
            ["Positive", "Negative", "Neutral"],
            [positive, negative, neutral]
        )
        ax2.set_title("Sentiment Comparison")
        ax2.set_ylabel("Count")
        st.pyplot(fig2)

else:
    st.warning("No data available to display dashboard.")


# Export Reports................................SECTION 5 

st.markdown("---")
st.subheader("📁 Export Reports")

conn = sqlite3.connect("database/processor.db")
full_df = pd.read_sql_query("SELECT * FROM texts", conn)
conn.close()

# Download Full Database
if not full_df.empty:
    csv_full = full_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Full Database",
        data=csv_full,
        file_name="full_batch_export.csv",
        mime="text/csv"
    )

# Download Filtered Results
if "filtered_data" in st.session_state:
    filtered_df = st.session_state["filtered_data"]

    if not filtered_df.empty:
        csv_filtered = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Filtered Results",
            data=csv_filtered,
            file_name="filtered_results_export.csv",
            mime="text/csv"
        )

# Download Summary Report
if not full_df.empty:

    positive = len(full_df[full_df["sentiment_score"] > 0])
    negative = len(full_df[full_df["sentiment_score"] < 0])
    neutral = len(full_df[full_df["sentiment_score"] == 0])
    total = len(full_df)
    avg_score = full_df["sentiment_score"].mean()

    summary_df = pd.DataFrame({
        "Metric": [
            "Total Records",
            "Positive Count",
            "Negative Count",
            "Neutral Count",
            "Average Sentiment Score"
        ],
        "Value": [
            total,
            positive,
            negative,
            neutral,
            round(avg_score, 2)
        ]
    })

    csv_summary = summary_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Summary Report",
        data=csv_summary,
        file_name="summary_report.csv",
        mime="text/csv"
    )