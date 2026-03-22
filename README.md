# Python-Parallel-Text-Handling-Processor

The Python Parallel Text Handling Processor is a system designed to efficiently process large volumes of text using parallel computing techniques. The application performs sentiment analysis, compares sequential vs parallel execution performance, and provides a visual analytics dashboard for insights.
The system demonstrates how multithreading and multiprocessing can improve text processing performance when working with large datasets.
This project is implemented using Python, Streamlit, SQLite, and Pandas.
# Python Parallel Text Handling Processor

 ## 🔷 Key Features

### 1. Text Processing System

* Upload `.txt`, `.csv`, `.xlsx` files
* Configurable **chunk-based text processing**
* Character-based chunking for large text handling

### 2. Sentiment Analysis Engine

* Rule-based sentiment scoring
* Weighted positive and negative word rules
* Automatic classification into:

  * Positive
  * Negative
  * Neutral

### 3. Parallel Processing Comparison

The system compares three processing approaches:

* Sequential Processing
* Thread-based Parallel Processing
* Multiprocessing-based Parallel Processing

Execution time is measured and displayed to analyze performance improvements.

### 4. Performance Benchmarking

* Displays execution time for each processing method
* Shows improvement percentage of parallel execution over sequential processing
* Designed to support large-scale text processing.

### 5. Database Storage

All processed text chunks are stored in an **SQLite database** with:

* Text chunk
* Sentiment score
* Sentiment tag
* Timestamp

Bulk insertion is implemented to improve performance when storing large datasets.

### 6. Sentiment Analytics Dashboard

A professional dashboard built with **Streamlit** that displays:

* Total processed records
* Average sentiment score
* Positive / Negative / Neutral counts
* Sentiment distribution charts

Charts include:

* Pie Chart for sentiment distribution
* Bar Chart for sentiment comparison

### 7. PDF Report Generation

The system can generate a **professional PDF report** summarizing:

* Sentiment statistics
* Processing performance
* Execution time comparison

### 8. Email Report Export

Generated reports can be automatically sent via **email with PDF attachment**.

---

## 🔷 System Architecture

The project follows a **modular architecture**:

```
Python Parallel Text Handling Processor
│
├── app.py                  # Streamlit main application
│
├── core
│   ├── chunker.py          # Text chunking logic
│   ├── rule_engine.py      # Sentiment scoring rules
│   ├── search_engine.py    # Search & filter functionality
│   ├── storage.py          # Database operations
│   ├── report_generator.py # PDF report generation
│   └── email_sender.py     # Email sending module
│
├── database
│   └── processor.db        # SQLite database
│
├── reports                 # Generated PDF reports
│
└── README.md
```

## 🔷 Technologies Used

* Python
* Streamlit
* SQLite
* Pandas
* Matplotlib
* ReportLab
* Multiprocessing
* Threading

## 🔷 Installation

Clone the repository:

```bash
git clone https://github.com/rohantarade22/Python-Parallel-Text-Handling-Processor.git
cd Python-Parallel-Text-Handling-Processor
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🔷 Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

## 🔷 Workflow

1. Upload a `.txt` file
2. Configure chunk size
3. Start processing
4. System performs:

   * Sentiment scoring
   * Parallel execution benchmarking
   * Database storage
5. View analytics on the dashboard
6. Generate and export a PDF report
7. send report via email(dummy)

---

## 🔷 Performance Optimization Implemented

* Chunk-based text processing
* Thread-based parallel execution
* Multiprocessing execution
* Bulk database insertion
* Efficient SQLite storage

These optimizations allow the system to handle **large text datasets efficiently**.

---

## 🔷 Future Improvements

Possible enhancements include:

* Machine learning based sentiment analysis
* NLP models for better accuracy
* Interactive charts using Plotly
* Large-scale distributed processing
* API integration for automated text ingestion

---

## Author

Rohan Tarade

GitHub Repository:
https://github.com/rohantarade22/Python-Parallel-Text-Handling-Processor

---

## License

This project is licensed under the MIT License © 2026 Rohan Tarade.
