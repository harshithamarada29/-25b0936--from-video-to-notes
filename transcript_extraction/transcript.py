import re
import json
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

def extract_video_id(url):              #get video_id from url
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return url

def clean_text(text):                    #removing multiple spaces 
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s([?.!,])", r"\1", text)
    return text.strip()

def main():
    url = input("Enter YouTube video URL: ").strip()
    video_id = extract_video_id(url)

    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)

        print("\nAvailable transcript languages:\n")   #print all available languages

        available = []
        i = 0
        for t in transcript_list:
            kind = "Auto" if t.is_generated else "Manual"
            print(f"{i}. {t.language} ({t.language_code}) - {kind}")
            available.append(t)
            i += 1

        choice = int(input("\nSelect language number: ")) #select the language in which you want transcript
        transcript = available[choice]

        segments = transcript.fetch()

    except (NoTranscriptFound, IndexError, ValueError):   
        print("Invalid selection or no transcript available")
        return

    raw_data = [                           #saving .json file
        {
            "text": seg.text,
            "start": seg.start,
            "duration": seg.duration
        }
        for seg in segments
    ]

    with open(f"{video_id}.json", "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)

    texts = [seg.text for seg in segments if seg.text.strip()]  #saving .txt file
    merged_text = " ".join(texts)
    cleaned_text = clean_text(merged_text)

    if cleaned_text:
        with open(f"{video_id}.txt", "w", encoding="utf-8") as f:
            f.write(cleaned_text)
        print("Saved .txt and .json files")
    else:
        print("Transcript fetched but cleaning is not done")

if __name__ == "__main__":     #run
    main()

                #make languages show in streamlit for the user#

def get_available_languages(url):
    video_id = extract_video_id(url)
    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)

    options = []
    for i, t in enumerate(transcript_list):
        kind = "Auto" if t.is_generated else "Manual"
        options.append({
            "index": i,
            "label": f"{t.language} ({t.language_code}) - {kind}"
        })

    return options

def extract_transcript_for_streamlit(url, choice_index):
    video_id = extract_video_id(url)
    api = YouTubeTranscriptApi()

    try:
        transcript_list = list(api.list(video_id))  
        transcript = transcript_list[choice_index]
        segments = transcript.fetch()

    except (NoTranscriptFound, IndexError, ValueError):
        return ""

    texts = [seg.text for seg in segments if seg.text.strip()]
    merged_text = " ".join(texts)
    cleaned_text = clean_text(merged_text)

    return cleaned_text