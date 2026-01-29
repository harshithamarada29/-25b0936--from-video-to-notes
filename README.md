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
-> Displays results in **four organized tabs** using NLP models:
  1. Chunk-wise Summaries
  2. Final Summary
  3. Bullet Points
  4. Keywords

->Displays results in **three organized tabs** using Gemini AI:
  1. Final Summary
  2. Bullet Points
  3. Keywords
     
-> Bullet points are generated using Gemini AI and rule-based sentence segmentation

-> Keywords are extracted using Gemini AI and **TF-IDF (classical NLP technique)**

-> Download options for:
  - Notes using NLP models
  - Notes using Gemini AI

`IMP NOTE: The user have to create a .env file in the root directory of the project. And mention GOOGLE_API_KEY="your google api key" in the .env file and save it.This is essestinal to get enhanced Gemini AI summary, keywords and some bullet points.`

-> This project uses Gemini 2.5 Flash to generate summary, bullet points and keywords

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
  - Gemini AI (for enhanced notes)
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
