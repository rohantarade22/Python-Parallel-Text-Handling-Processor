import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from core.storage import create_database, clear_database, bulk_insert
from core.rule_engine import score_text
from core.search_engine import search_data
from core.report_generator import generate_pdf_report
from core.email_sender import send_email
from core.chunker import split_into_chunks

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Text Processor", layout="wide")
create_database()

# ---------------- DARK MODE ----------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.markdown('<div class="sidebar-title">🚀 Command Center</div>', unsafe_allow_html=True)
    st.caption("Parallel Text Processing System")

    st.markdown('<div class="sidebar-section">Main</div>', unsafe_allow_html=True)

    page = st.radio(
        "",
        [
            "🏠 Home",
            "⚙️ Process Data",
            "📂 View Data",
            "📊 Dashboard",
            "🔍 Search",
            "📁 Export & Email"
        ]
    )

    st.markdown("---")

    st.markdown('<div class="sidebar-section">Settings</div>', unsafe_allow_html=True)

    dark_mode = st.toggle("🌙 Dark Mode")
    st.session_state.dark_mode = dark_mode

    st.markdown("---")
    st.caption("⚡ Engineered for Performance")

# ---------------- CSS ----------------
if st.session_state.dark_mode:
    st.markdown("""
    <style>
    .stApp { 
        background-color: #0E1117; 
        color: white; 
    }

    /* Sidebar background */
    section[data-testid="stSidebar"] { 
        background-color: #111827 !important; 
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    header[data-testid="stHeader"] {
        background-color: #0E1117 !important;
    }

    /* Toolbar (top right icons area) */
    div[data-testid="stToolbar"] {
        background-color: #0E1117 !important;
    }
                
    /* Fix radio button labels */
    .stRadio label {
        color: white !important;
    }

    /* Sidebar title */
    .sidebar-title { 
        color: white !important; 
        font-size: 20px; 
        font-weight: 600;
    }

    /* Sidebar section labels */
    .sidebar-section {
        color: #9CA3AF !important;
        font-size: 12px;
        margin-top: 15px;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }

    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E5E7EB;
    }

    section[data-testid="stSidebar"] * {
        color: #111827 !important;
    }

    .sidebar-title { 
        font-size: 20px; 
        font-weight: 600; 
    }

    .sidebar-section {
        font-size: 12px;
        color: #6B7280;
        margin-top: 15px;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- HOME ----------------
if page == "🏠 Home":
    st.title("🚀 Parallel Text Processor")
    st.caption("Fast • Scalable • Text Processing System")
    st.success("👈 Upload  your TXT, CSV or Excel file and analyze sentiment efficiently.")

    st.markdown("---")

    st.subheader("✨ Key Features")
    col1, col2, col3 = st.columns(3)

    col1.markdown("**⚡ Parallel Processing**\n- Threading\n- Multiprocessing")
    col2.markdown("**📊 Sentiment Analysis**\n- Positive / Negative / Neutral\n-  Score-based classification")
    col3.markdown("**📁 Data Management**\n- Database storage \n- Efficient searching \n- Export & reports ")

    st.markdown("---")

    st.subheader("📌User Guide")

    st.markdown("""
    1. Go to **⚙️ Process Data**  
    2. Upload your file (.txt / .csv / .xlsx)  
    3. Click **Start Processing**  
    4. View results in **Dashboard**  
    5. Export or Email reports  
    """)

    st.markdown("---")

    st.subheader("📘 Guidelines")

    st.markdown("""
    - Ensure clean text data   
    - Smaller chunk size = detailed analysis  
    """)
    st.markdown("---")


# ---------------- PROCESS ----------------
elif page == "⚙️ Process Data":

    st.title("⚙️ Process File")

    file = st.file_uploader("Upload File", type=["txt", "csv", "xlsx"])

    if file:
        ext = file.name.split(".")[-1]

        if ext == "txt":
            text = file.read().decode("utf-8")
        elif ext == "csv":
            df = pd.read_csv(file)
            text = "\n".join(df.iloc[:, 0].astype(str))
        elif ext == "xlsx":
            df = pd.read_excel(file)
            text = "\n".join(df.iloc[:, 0].astype(str))
        else:
            st.error("Unsupported file")
            text = ""

        st.success("File uploaded successfully ✅")
        if not text.strip():
            st.error("⚠️ Uploaded file is empty. Please upload valid data.")
            st.stop()

        # ✅ ADDED CLEAR OPTION
        clear_option = st.checkbox("Clear Previous Data")

        if st.button("🚀 Start Processing"):

            if clear_option:
                clear_database()
                st.warning("Previous data cleared")

            chunks = split_into_chunks(text)

            # ✅ PROGRESS BAR
            # ✅ PROGRESS BAR
            progress = st.progress(0)
            status = st.empty()

            total_steps = len(chunks) * 3
            step = 0

            # -------- SEQUENTIAL --------
            start_seq = time.time()
            seq_scores = []

            for c in chunks:
                seq_scores.append(score_text(c))

                time.sleep(0.005)  # smooth UI

                step += 1
                percent = int((step / total_steps) * 100)

                progress.progress(step / total_steps)
                status.markdown(f"### ⏳ {percent}% Completed")

            sequential_time = time.time() - start_seq


            # -------- THREADING --------
            start_thread = time.time()
            thread_scores = []

            with ThreadPoolExecutor() as ex:
                for res in ex.map(score_text, chunks):
                    thread_scores.append(res)

                    step += 1
                    percent = int((step / total_steps) * 100)

                    progress.progress(step / total_steps)
                    status.markdown(f"### ⏳ {percent}% Completed")

            threading_time = time.time() - start_thread


            # -------- MULTIPROCESSING --------
            start_proc = time.time()
            process_scores = []

            with ProcessPoolExecutor() as ex:
                for res in ex.map(score_text, chunks):
                    process_scores.append(res)

                    step += 1
                    percent = int((step / total_steps) * 100)

                    progress.progress(step / total_steps)
                    status.markdown(f"### ⏳ {percent}% Completed")

            multiprocessing_time = time.time() - start_proc


            # ✅ FINISH
            progress.progress(1.0)
            status.markdown("### ✅ Processing Completed")

            # Store
            records = []
            for c, s in zip(chunks, process_scores):
                tag = "Positive" if s > 0 else "Negative" if s < 0 else "Neutral"
                records.append((c, s, tag))

            bulk_insert(records)

            st.success("Processing Completed 🎉")

            # Performance Metrics
            st.markdown("### ⏱ Performance Comparison")

            col1, col2, col3 = st.columns(3)
            col1.metric("Sequential Time", round(sequential_time, 4))
            col2.metric("Threading Time", round(threading_time, 4))
            col3.metric("Multiprocessing Time", round(multiprocessing_time, 4))

# ---------------- VIEW DATA ----------------
elif page == "📂 View Data":

    st.title("📂 Database Records")

    conn = sqlite3.connect("database/processor.db")
    df = pd.read_sql_query("SELECT * FROM texts", conn)
    conn.close()

    if not df.empty:

        # ✅ ADDED METRICS
        total = len(df)
        pos = len(df[df["sentiment_score"] > 0])
        neg = len(df[df["sentiment_score"] < 0])
        neu = len(df[df["sentiment_score"] == 0])

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Records", total)
        col2.metric("Positive", pos)
        col3.metric("Negative", neg)
        col4.metric("Neutral", neu)

        st.dataframe(df, use_container_width=True)

        sentiment = st.selectbox("Filter by Sentiment", ["All", "Positive", "Negative", "Neutral"])

        if sentiment != "All":
            df = df[df["tags"] == sentiment]

        st.dataframe(df.head(50), use_container_width=True)

    else:
        st.warning("No data")

# ---------------- DASHBOARD ----------------
elif page == "📊 Dashboard":

    st.title("📊 Sentiment Dashboard")

    conn = sqlite3.connect("database/processor.db")
    df = pd.read_sql_query("SELECT * FROM texts", conn)
    conn.close()

    if not df.empty:

        pos = len(df[df["sentiment_score"] > 0])
        neg = len(df[df["sentiment_score"] < 0])
        neu = len(df[df["sentiment_score"] == 0])

        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots()
            ax.pie([pos, neg, neu], labels=["Positive", "Negative", "Neutral"], autopct="%1.1f%%")
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots()
            ax.bar(["Positive", "Negative", "Neutral"], [pos, neg, neu])
            st.pyplot(fig)

        st.markdown("### 📌 Summary")
        st.write(f"Total Records: {len(df)}")
        st.write(f"Positive: {pos} | Negative: {neg} | Neutral: {neu}")

    else:
        st.warning("No data")

# ---------------- SEARCH ----------------
elif page == "🔍 Search":

    st.title("🔍 Search Data")

    col1, col2 = st.columns(2)

    with col1:
        keyword = st.text_input("Keyword")

    col3, col4 = st.columns(2)

    with col3:
        min_score = st.text_input("Min Score")

    with col4:
        max_score = st.text_input("Max Score")

    if st.button("Search"):

        min_val = int(min_score) if min_score else None
        max_val = int(max_score) if max_score else None

        df = search_data(keyword, min_val, max_val)

        st.success(f"Results Found: {len(df)}")
        st.dataframe(df, use_container_width=True)

# ---------------- EXPORT ----------------
elif page == "📁 Export & Email":

    st.title("📁 Export & Email")

    conn = sqlite3.connect("database/processor.db")
    df = pd.read_sql_query("SELECT * FROM texts", conn)
    conn.close()

    if not df.empty:

        st.subheader("📥 Download Data")

        st.download_button("Download Full Data (CSV)", df.to_csv(index=False), "full_data.csv")

        pos = len(df[df["sentiment_score"] > 0])
        neg = len(df[df["sentiment_score"] < 0])
        neu = len(df[df["sentiment_score"] == 0])

        pdf = generate_pdf_report(len(df), pos, neg, neu, 0, 0, 0)

        with open(pdf, "rb") as f:
            st.download_button("Download Summary Report (PDF)", f, "summary.pdf")

        st.markdown("---")

        st.subheader("📧 Send Report via Email")

        email = st.text_input("Enter Email")

        if st.button("Send Email"):
            send_email(email, pdf)
            st.success("Email Sent (Simulation) ✅")

    else:
        st.warning("No data")