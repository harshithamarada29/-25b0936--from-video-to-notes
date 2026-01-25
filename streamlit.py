import streamlit as st
from transcript_extraction.transcript import (
    get_available_languages,
    extract_transcript_for_streamlit
)
from summarize_the_transcript.summarize import (
    summarize_text,
    generate_bullet_points,
    extract_keywords
)

st.set_page_config(
    page_title="Video to Notes",
    layout="wide"
)

st.title("Video to Notes")
st.caption("Paste a YouTube video url or video id, select language, and generate notes automatically")

                                #Sidebar#
st.sidebar.header(" Give your Inputs here ")

video_url = st.sidebar.text_input(
    "Enter YouTube Video ID or URL link",
    placeholder="Eg: https://www.youtube.com/watch?v=XXXX"
)

fetch_lang = st.sidebar.button("Fetch Languages")

                                #Session states#
if "languages" not in st.session_state:
    st.session_state.languages = None
if "selected_index" not in st.session_state:
    st.session_state.selected_index = None
if "transcript_text" not in st.session_state:
    st.session_state.transcript_text = None
if "results" not in st.session_state:
    st.session_state.results = None

                        #Ask for user's wanted transcript language
if fetch_lang:
    if not video_url.strip():
        st.sidebar.warning("Please enter a valid video URL / ID")
    else:
        with st.spinner("Fetching available transcript languages..Please wait"):
            st.session_state.languages = get_available_languages(video_url)

        if not st.session_state.languages:
            st.sidebar.error("No transcript languages found")
        else:
            st.sidebar.success("Languages fetched successfully")

if st.session_state.languages:
    labels = [lang["label"] for lang in st.session_state.languages]

    selected = st.sidebar.selectbox(
        "Select Transcript Language",
        labels
    )

    st.session_state.selected_index = labels.index(selected)

    generate = st.sidebar.button("Generate Summary")

    if generate:
        with st.status("Processing video..Please wait",expanded=True) as status:
            status.write("Extracting transcript...")
            transcript_text = extract_transcript_for_streamlit(
                video_url,
                st.session_state.selected_index
            )

            if not transcript_text:
                status.update(label="Transcript extraction failed", state="error")
            else:
                status.write("Please wait..Generating Summary..It may take some time")
                chunk_summaries, final_summary = summarize_text(transcript_text)

                st.session_state.results = (chunk_summaries, final_summary)
                status.update(label="Notes generation successful..!!", state="complete")

if st.session_state.results:
    chunk_summaries, final_summary = st.session_state.results

    st.divider()
    st.header("Generated Results")
                    #Using tabs for chunk summaries and final summary#
    tab1, tab2, tab3, tab4 = st.tabs(
        [" Chunk-wise Summaries ", " Final Summary ", " Bullet Points ", " Keywords "]
    )

    with tab1:
        for i, chunk in enumerate(chunk_summaries, start=1):
            with st.expander(f"Chunk {i}"):
                st.write(chunk)

    with tab2:
        st.write(final_summary)

    with tab3:
        bullets = generate_bullet_points(final_summary)
        for b in bullets:
            st.write("•", b)

    with tab4:
        keywords = extract_keywords(final_summary)
        for k in keywords:
            st.write("•", k)

                         #Download the generated summary#
    st.divider()
    st.subheader(" Download below")

    chunks_text = "\n\n".join(
        [f"Chunk {i+1}\n{c}" for i, c in enumerate(chunk_summaries)]
    )

    st.download_button(
        "Download Chunk Summaries",
        chunks_text,
        file_name="chunk_summaries.txt"
    )
    st.download_button(
        "Download Final Summary",
        final_summary,
        file_name="final_summary.txt"
    )