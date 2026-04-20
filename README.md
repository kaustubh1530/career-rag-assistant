# Career RAG Assistant

An AI-powered **career document assistant** that uses **Retrieval-Augmented Generation (RAG)** to compare a resume against multiple internship/job description PDFs and generate grounded career insights.

---

## Overview

This project ingests multiple PDFs such as:
- a candidate resume
- software engineering internship job descriptions
- backend/software internship job descriptions
- machine learning internship job descriptions

It then:
1. extracts text from all PDFs
2. splits them into chunks
3. converts chunks into embeddings
4. stores them in **FAISS**
5. retrieves the most relevant chunks for a user question
6. uses **OpenAI** to generate a grounded answer

This creates a practical **AI Career Assistant** that can help with:
- resume-job matching
- identifying missing keywords
- skill comparison
- project alignment
- career improvement suggestions

---

## Tech Stack

- **Python**
- **OpenAI API**
- **FAISS**
- **NumPy**
- **PyPDF**
- **python-dotenv**

---

## Project Structure

```text
career-rag-assistant/
├── app.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── documents/
├── extracted_texts/
├── screenshots/
└── venv/
```

---

## How It Works

### 1. Multi-Document Ingestion
The app automatically loads every PDF from the `documents/` folder.

### 2. Text Extraction
Each PDF is read and converted into plain text.

### 3. Chunking
Large text is split into smaller chunks so it can be processed effectively.

### 4. Embeddings
Each chunk is converted into a vector using OpenAI embeddings.

### 5. FAISS Vector Search
Embeddings are stored in FAISS for semantic similarity search.

### 6. Grounded Answer Generation
The most relevant chunks are passed to OpenAI, which generates a context-based answer.

---

## Example Use Cases

This project can be adapted for:
- resume analysis
- job matching
- document Q&A
- internal knowledge assistants
- career coaching tools

---

## Future Improvements

Potential upgrades:
- build a **Streamlit** or **Flask** web UI
- upload PDFs directly in the app
- display source document names for retrieved chunks
- add resume keyword gap analysis
- generate a job match score

---

## Author

**Kaustubh Patil**