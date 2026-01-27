import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

from transcript_extraction.transcript import (
    get_available_languages,
    extract_transcript_for_streamlit
)

from summarize_the_transcript.summarize import (
    summarize_text,
    generate_bullet_points,
    extract_keywords
)

load_dotenv()

# PAGE CONFIGURATION #
st.set_page_config(page_title="Video to Notes", layout="wide")

st.title("Video to Notes")
st.caption("Generate lecture notes using NLP models and Gemini AI")

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# SIDEBAR  #
st.sidebar.header("Give your Inputs here")

video_url = st.sidebar.text_input(
    "Enter YouTube Video URL / ID",
    placeholder="Eg: https://www.youtube.com/watch?v=XXXX"
)

fetch_lang = st.sidebar.button("Fetch Languages")

# SESSION STATES #
if "languages" not in st.session_state:
    st.session_state.languages = None
if "selected_index" not in st.session_state:
    st.session_state.selected_index = None
if "nlp_results" not in st.session_state:
    st.session_state.nlp_results = None
if "gemini_results" not in st.session_state:
    st.session_state.gemini_results = None
if "error" not in st.session_state:
    st.session_state.error = None

# FETCH LANGUAGES #
if fetch_lang:
    if not video_url.strip():
        st.sidebar.warning("Please enter a valid video URL / ID")
    else:
        with st.spinner("Fetching available transcript languages..."):
            st.session_state.languages = get_available_languages(video_url)

        if not st.session_state.languages:
            st.sidebar.error("No transcript languages found")
        else:
            st.sidebar.success("Languages fetched successfully")

# LANGUAGE SELECTION #
if st.session_state.languages:
    labels = [lang["label"] for lang in st.session_state.languages]

    selected = st.sidebar.selectbox(
        "Select Transcript Language",
        labels
    )

    st.session_state.selected_index = labels.index(selected)

    generate = st.sidebar.button("Generate Notes")

    if generate:
        with st.status("Processing video...Please wait", expanded=True) as status:
            status.write("Extracting transcript...")

            transcript_text = extract_transcript_for_streamlit(
                video_url,
                st.session_state.selected_index
            )

            if not transcript_text:
                st.session_state.error = "Transcript extraction failed"
                status.update(label="Transcript extraction failed", state="error")

            else:
                # -------- NLP MODE -------- #
                status.write("Generating notes using NLP models...")

                chunk_summaries, final_summary = summarize_text(transcript_text)
                bullets = generate_bullet_points(final_summary)
                keywords = extract_keywords(final_summary)

                st.session_state.nlp_results = {
                    "chunks": chunk_summaries,
                    "summary": final_summary,
                    "bullets": bullets,
                    "keywords": keywords
                }

                # -------- GEMINI MODE -------- #
                status.write("Generating notes using Gemini AI...")

                try:
                    # Gemini summary
                    prompt_summary = f"""
You are an expert academic note-making assistant.

From the following lecture transcript:
1. Identify the main topics discussed.
2. Write a STRUCTURED SUMMARY using clear topic-wise subheadings.
3. Under each subheading, write a short paragraph (3–5 lines).
4. Use simple, student-friendly academic language.
5. Do NOT copy sentences directly from the transcript.
6. Do NOT add any introduction or conclusion outside the topics.

Formatting rules:
- Use Markdown headings for topics (## Topic Name)
- Paragraphs should be concise and explanatory

Transcript:
{transcript_text}
"""
                    gem_summary = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt_summary
                    ).text

                    # Gemini bullets
                    prompt_bullets = f"""
Generate clean bullet-point notes from the transcript.
Rules:
- One key idea per bullet
- Exam-oriented language
- No extra explanations

Transcript:
{transcript_text}
"""
                    gem_bullets = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt_bullets
                    ).text

                    # Gemini keywords
                    prompt_keywords = f"""
Extract important keywords from the transcript.
Rules:
- 1–3 word phrases
- No sentences

Transcript:
{transcript_text}
"""
                    gem_keywords = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt_keywords
                    ).text

                    st.session_state.gemini_results = {
                        "summary": gem_summary,
                        "bullets": gem_bullets,
                        "keywords": gem_keywords
                    }

                    status.update(label="Notes generated successfully", state="complete")
                    st.toast("Your notes are ready 🧠")
                    st.snow()

                except Exception as e:
                    st.session_state.error = str(e)
                    status.update(label="Gemini processing failed..Your token limit might be exceeded..Please visit after some time..!", state="error")

# ERROR #
if st.session_state.error:
    st.error(st.session_state.error)

# FINAL RESULTS SCREEN #
if st.session_state.nlp_results:

    st.divider()
    st.header("Generated Results")

    model_tab1, model_tab2 = st.tabs(
        [" NLP Models ", " Gemini AI "]
    )

    # ---------- NLP VIEW ---------- #
    with model_tab1:
        nlp = st.session_state.nlp_results

        tab1, tab2, tab3, tab4 = st.tabs(
            ["Chunk-wise Summaries", "Final Summary", "Bullet Points", "Keywords"]
        )

        with tab1:
            for i, chunk in enumerate(nlp["chunks"], start=1):
                with st.expander(f"Chunk {i}"):
                    st.write(chunk)

        st.download_button(
            "Download Chunk Summaries",
            "\n\n".join(
                [f"Chunk {i+1}\n{c}" for i, c in enumerate(nlp["chunks"])]
            ),
            file_name="nlp_chunk_summaries.txt"
        )

        with tab2:
            st.write(nlp["summary"])

        st.download_button(
            "Download Final summary",
            nlp["summary"],
            file_name="nlp_final_summary.txt"
        )

        with tab3:
            for b in nlp["bullets"]:
                st.write("•", b)

        st.download_button(
            "Download Bullet Points",
            "\n".join(nlp["bullets"]),
            file_name="nlp_bullet_points.txt"
        )

        with tab4:
            for k in nlp["keywords"]:
                st.write("•", k)

        st.download_button(
            "Download Keywords",
            "\n".join(nlp["keywords"]),
            file_name="nlp_keywords.txt"
        )

    # ---------- GEMINI VIEW ---------- #
    with model_tab2:

        if st.session_state.gemini_results:
            gem = st.session_state.gemini_results

            tab1, tab2, tab3 = st.tabs(
                ["Final Summary", "Bullet Points", "Keywords"]
            )

            with tab1:
                st.markdown(gem["summary"])   # markdown for topic headings

            st.download_button(
                "Download Summary",
                gem["summary"],
                file_name="gemini_summary.txt"
            )

            with tab2:
                st.write(gem["bullets"])

            st.download_button(
                "Download Bullet points",
                gem["bullets"],
                file_name="gemini_bullets.txt"
            )

            with tab3:
                st.write(gem["keywords"])

            st.download_button(
                "Download Keywords",
                gem["keywords"],
                file_name="gemini_keywords.txt"
            )

        else:
            st.warning(
                "Gemini summary not available (daily limit may be exceeded)"
            )
