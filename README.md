**Video to Notes — Transcript Extraction & Summarization**

This project converts YouTube lecture videos into clean text and meaningful summaries using Python and NLP models.  
It is implemented in two milestones.

**Milestone 1 — Transcript Extraction**

#Extracts subtitles from YouTube videos using **youtube-transcript-api**
  - Manually created captions
  - Auto-generated captions
#Saves output in two formats
.json file - raw transcript with timestamps  
.txt file - cleaned readable text

**Milestone 2 — Summarization Engine**

#Takes transcript text as input  
# Summarizes:
  - Each chunk separately
  - Then all summaries again to create a **final summary**

**Model usage**
#**English** → `facebook/bart-large-cnn`  
#**Other languages** → `google/mt5-small`

Note: This works more efficiently for the transcript in English language.
