# Imports the library
from datetime import timedelta
from pytube import YouTube
import whisper

# Ask the youtube video link
link = input("Your video link :")

# Recuperate the video with the link
yt = YouTube(link)

# Download the video
yt.streams.filter(file_extension='mp4').first().download()
filename = yt.streams.filter(file_extension='mp4').first().default_filename

# Load the model
model = whisper.load_model("base")
print("Whisper model loaded.")

# Transcribe the video audio
transcribe = model.transcribe(filename)
segments = transcribe['segments']

# Create a file .srt with the name of the video
f = open(f"{filename}.srt", "x")

# For each segments of audio
for segment in segments:
    # The start of the audio
    startTime = str(0) + str(timedelta(seconds=int(segment['start']))) + ',000'
    
    # The end of the audio
    endTime = str(0) + str(timedelta(seconds=int(segment['end']))) + ',000'

    # The text of the segment
    text = segment['text']

    # The Id of the segment
    segmentId = segment['id']+1

    # The line for the subtitles in the .srt file
    segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] is ' ' else text}\n\n"

    # Open the .srt file
    with open(f"{filename}.srt", 'a', encoding='utf-8') as srtFile:
        # Write the segment line in it
        srtFile.write(segment)
