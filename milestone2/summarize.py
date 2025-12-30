from transformers import pipeline
import os

summarizer = pipeline(                             #loading model
    "summarization",
    model="facebook/bart-large-cnn"
)

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
    summary = summarizer(
        chunk,
        max_length=150,
        min_length=60,
        do_sample=False
    )
    return summary[0]["summary_text"]

def final_summarize(chunks, output_file):            #heirarchial summary
    print("Intermediate Chunk Summaries")

    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        s = summarize_chunk(chunk)
        chunk_summaries.append(s)
        print(f"Chunk {i+1} summary: {s}\n")

    merged_text = " ".join(chunk_summaries)

    print(" Final Summary ")
    final = summarize_chunk(merged_text)
    print(final)

    with open(output_file, "w", encoding="utf-8") as f:         #save final summary
        f.write(final)

    print(f"Final summary saved to {output_file}")
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
    output_file = f"{base_name}_summary.txt"

    chunks = chunk_text(long_text)
    final_summarize(chunks, output_file)