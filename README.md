# Video to Notes — Transcript Extraction & Summarization

This project converts YouTube lecture videos into clean text and meaningful notes using Python and NLP techniques.
It automates the process of watching long lectures by extracting transcripts and generating structured summaries.

---

## Milestone 1 — Transcript Extraction

->Extracts subtitles from YouTube videos using `youtube-transcript-api`

->Supports:
  - Manually created captions
  - Auto-generated captions
  - 
->Allows the user to select the preferred transcript language

->Saves output in two formats:
  - `.json` file — raw transcript with timestamps
  - `.txt` file — cleaned and readable transcript text

---

## Milestone 2 — Summarization Engine

-> Takes transcript text as input

-> Uses a **chunk-based summarization strategy**:
  - Each chunk is summarized separately
  - All chunk summaries are then summarized again to produce a final summary
    
-> Handles long transcripts efficiently

### Models Used
- **English transcripts** → `facebook/bart-large-cnn`
- **Other languages** → `google/mt5-small`

> **Note:** The summarization works most efficiently for transcripts in the English language.

---

## Milestone 3 — Interactive Streamlit Web Interface

-> A clean and interactive web UI built using **Streamlit**

-> Eliminates the need for command-line interaction

-> Allows users to:
  - Enter a YouTube video URL or ID
  - Fetch all available transcript languages
  - Select the desired language
  - Generate notes with a single click

### Features
-> Displays results in **four organized tabs**:
  1. Chunk-wise Summaries
  2. Final Summary
  3. Bullet Points
  4. Keywords
     
-> Bullet points are generated using rule-based sentence segmentation

-> Keywords are extracted using **TF-IDF (classical NLP technique)**

-> Download options for:
  - Chunk summaries
  - Final summary

---

## Tech Stack

- **Language:** Python
- **Libraries:**
  - youtube-transcript-api
  - transformers
  - torch
  - streamlit
  - scikit-learn
  - langdetect
- **Models:**
  - BART (English summarization)
  - mT5 (Multilingual summarization)

---

## Project Structure

```text
video-to-notes/
├── transcript_extraction/
│   └── transcript.py
├── summarize_the_transcript/
│   └── summarize.py
├── streamlit.py
├── README.md
