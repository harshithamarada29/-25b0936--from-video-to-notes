from transformers import pipeline
import os
import re
from langdetect import detect
from sklearn.feature_extraction.text import TfidfVectorizer

english_summarizer = pipeline(                             #loading bart model
    "summarization",
    model="facebook/bart-large-cnn"
)

multilingual_summarizer = pipeline(                        #loading mt5 model
    "summarization",
    model="google/mt5-small"
)

def get_summarizer(text):                                  #choose model based on language
    try:
        lang = detect(text)
    except:
        lang = "en"

    if lang == "en":
        return english_summarizer
    else:
        return multilingual_summarizer

def chunk_text(text, chunk_size=1200, overlap=150):     #break model into chunks
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks

def summarize_chunk(chunk):                         #summarize each chunk
    model = get_summarizer(chunk)
    summary = model(
        chunk,
        max_length=230,
        min_length=110,
        do_sample=False
    )
    return summary[0]["summary_text"]

def final_summarize(chunks, base_name):            #heirarchial summary
    print("Intermediate Chunk Summaries")

    # file names
    intermediate_file = f"{base_name}_chunk_summaries.txt"
    final_file = f"{base_name}_summary.txt"

    chunk_summaries = []

    with open(intermediate_file, "w", encoding="utf-8") as f_int:       #intermediate summary
        for i, chunk in enumerate(chunks):
            s = summarize_chunk(chunk)
            chunk_summaries.append(s)
            print(f"Chunk {i+1} summary: {s}\n")

            f_int.write(f"--- Chunk {i+1} Summary ---\n")
            f_int.write(s + "\n\n")

    merged_text = " ".join(chunk_summaries)

    print(" Final Summary ")

    final_chunks = chunk_text(merged_text, chunk_size=800, overlap=100)              #safe final summary
    final = summarize_chunk(final_chunks[0])
    print(final)

    with open(final_file, "w", encoding="utf-8") as f:         #save final summary
        f.write(final)

    print(f"Intermediate summaries saved to {intermediate_file}")
    print(f"Final summary saved to {final_file}")
    return final

if __name__ == "__main__":                                #main func
    file_path = input("Enter path to transcript text file: ").strip()

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            long_text = f.read()
    except FileNotFoundError:
        print("File not found.")
        exit()

    base_name = os.path.splitext(os.path.basename(file_path))[0]    #giving output file name

    chunks = chunk_text(long_text)
    final_summarize(chunks, base_name)
    
                       #summarization code for streamlit#

def summarize_text(text):
    chunks = chunk_text(text)

    chunk_summaries = []
    for chunk in chunks:
        s = summarize_chunk(chunk)
        chunk_summaries.append(s)
    merged = " ".join(chunk_summaries)

    final_chunks = chunk_text(
        merged,
        chunk_size=1000,   # safe size
        overlap=120
    )

    final_summaries = []
    for fc in final_chunks:
        fs = summarize_chunk(fc)
        final_summaries.append(fs)

    final_summary = " ".join(final_summaries)

    return chunk_summaries, final_summary

def generate_bullet_points(summary, max_points=8):
    sentences = re.split(r'(?<=[.!?])\s+', summary)
    bullets = [s.strip() for s in sentences if len(s.strip()) > 40]
    return bullets[:max_points]

def extract_keywords(text, top_k=10):
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=top_k
    )
    vectorizer.fit([text])
    return vectorizer.get_feature_names_out()