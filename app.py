from openai import OpenAI
from dotenv import load_dotenv
from pypdf import PdfReader
import os
import faiss
import numpy as np


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Please add it to your .env file.")

client = OpenAI(api_key=api_key)


DOCUMENTS_FOLDER = "documents"
EXTRACTED_FOLDER = "extracted_texts"
CHUNK_SIZE = 500
TOP_K = 4


def extract_text_from_pdfs(folder_path):
    all_text = ""
    document_names = []

    print("📂 Reading PDF files...\n")

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            reader = PdfReader(pdf_path)

            pdf_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    pdf_text += text + "\n"

            # Save extracted text
            txt_filename = filename.replace(".pdf", ".txt")
            txt_path = os.path.join(EXTRACTED_FOLDER, txt_filename)

            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(pdf_text)

            print(f"✅ Extracted: {filename}")
            document_names.append(filename)

            all_text += f"\n\n===== DOCUMENT: {filename} =====\n\n"
            all_text += pdf_text

    return all_text, document_names

def chunk_text(text, chunk_size=500):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
    return chunks

def get_embeddings(text_chunks):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text_chunks
    )
    return [item.embedding for item in response.data]


def main():
    all_text, document_names = extract_text_from_pdfs(DOCUMENTS_FOLDER)

    print("\n📄 All PDFs processed successfully!")
    print(f"📚 Total documents loaded: {len(document_names)}")

    chunks = chunk_text(all_text, chunk_size=CHUNK_SIZE)
    print(f"✅ Total chunks created: {len(chunks)}")

    chunk_embeddings = get_embeddings(chunks)
    embedding_matrix = np.array(chunk_embeddings).astype("float32")
    print(f"🔢 Embedding matrix shape: {embedding_matrix.shape}")

    # Store in FAISS
    dimension = embedding_matrix.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embedding_matrix)
    print("📦 All document chunks stored in FAISS successfully!")

    # Ask question
    query = input("\n❓ Ask a career-related question: ")

    query_embedding = get_embeddings([query])
    query_vector = np.array(query_embedding).astype("float32")

    # Search
    k = min(TOP_K, len(chunks))
    distances, indices = index.search(query_vector, k)

    print("\n🔍 Top matching chunks:\n")
    retrieved_chunks = []

    for rank, idx in enumerate(indices[0]):
        if idx == -1:
            continue

        print(f"--- Match {rank + 1} (Chunk #{idx}) ---")
        print(f"Distance Score: {distances[0][rank]:.4f}")
        print(chunks[idx][:500])
        print("\n")

        retrieved_chunks.append(chunks[idx])

    # Combine context
    context = "\n\n".join(retrieved_chunks)

    # Final LLM answer
    chat_response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are a helpful AI career assistant.

Answer only using the provided context from the candidate's resume and job description PDFs.

Your job is to help with:
- resume-job matching
- skill comparison
- identifying missing keywords
- summarizing qualifications
- suggesting what the candidate should improve

If the answer is not clearly in the context, say:
'I could not find that information clearly in the provided documents.'
"""
            },
            {
                "role": "user",
                "content": f"""
Use the context below to answer the question.

Context:
{context}

Question:
{query}

Answer clearly, professionally, and in a helpful way.
"""
            }
        ]
    )

    final_answer = chat_response.choices[0].message.content

    print("\n🤖 Final AI Career Answer:\n")
    print(final_answer)

if __name__ == "__main__":
    main()