from transformers import pipeline
import os
from langdetect import detect

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
    limit = min(len(merged), 4000)     #dynamic limit

    final_summary = summarize_chunk(merged[:limit])

    return chunk_summaries, final_summary