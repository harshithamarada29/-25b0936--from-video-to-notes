import re
import json
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

def extract_video_id(url):   # get video id from url
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return url

def clean_text(text):        # cleaning text
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s([?.!,])", r"\1", text)
    return text.strip()

def main():                  # extracting transcript
    url = input("Enter YouTube video URL: ").strip()
    video_id = extract_video_id(url)

    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)

        try:                  #language selection
            transcript = transcript_list.find_manually_created_transcript(["en"])
        except:
            try:
                transcript = transcript_list.find_generated_transcript(["en"])
            except:
                try:
                    transcript = transcript_list.find_generated_transcript(["hi"])
                except:
                    print("No transcript found in English or Hindi")
                    return

        segments = transcript.fetch()

    except NoTranscriptFound:
        print("No transcript available for this video")
        return

    raw_data = [                     #saving .json file
        {
            "text": seg.text,
            "start": seg.start,
            "duration": seg.duration
        }
        for seg in segments
    ]

    with open(f"{video_id}.json", "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)

    texts = [seg.text for seg in segments if seg.text.strip() != ""]     #saving .txt file
    merged_text = " ".join(texts)
    cleaned_text = clean_text(merged_text)

    if cleaned_text:
        with open(f"{video_id}.txt", "w", encoding="utf-8") as f:
            f.write(cleaned_text)
        print("Saved .txt and .json files")
    else:
        print("Transcript fetched but cleaning is not done")

if __name__ == "__main__":    # run
    main()