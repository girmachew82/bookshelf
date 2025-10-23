from youtube_transcript_api import YouTubeTranscriptApi

# Replace with your video ID (the part after v= in the URL)
video_id = "pTFZFxd4hOI&t=223s"

# Get transcript
transcript = YouTubeTranscriptApi.get_transcript(video_id)

# Print text only
for entry in transcript:
    print(entry['text'])
