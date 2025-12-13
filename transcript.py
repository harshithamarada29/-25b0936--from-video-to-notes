from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

video_id = input("Enter YouTube Video ID ").strip()

try:
    srt = YouTubeTranscriptApi().fetch(video_id)
except NoTranscriptFound:
    print("No transcript found for this video.")
    exit()

text = "\n".join([line.text for line in srt])

filename = f"{video_id}.txt"   #save transcript in name of video ID
with open(filename, "w", encoding="utf-8") as f:
    f.write(text)

print(f"Transcript saved to {filename}")