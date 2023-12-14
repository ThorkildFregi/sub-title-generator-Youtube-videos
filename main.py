from datetime import timedelta
from pytube import YouTube
import whisper

link = input("Your video link :")

yt = YouTube(link)

yt.streams.filter(file_extension='mp4').first().download()
filename = yt.streams.filter(file_extension='mp4').first().default_filename

model = whisper.load_model("base")
print("Whisper model loaded.")

transcribe = model.transcribe(filename)
segments = transcribe['segments']

f = open(f"{filename}.srt", "x")

for segment in segments:
    startTime = str(0) + str(timedelta(seconds=int(segment['start']))) + ',000'
    endTime = str(0) + str(timedelta(seconds=int(segment['end']))) + ',000'
    text = segment['text']
    segmentId = segment['id']+1
    segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] is ' ' else text}\n\n"

    with open(f"{filename}.srt", 'a', encoding='utf-8') as srtFile:
        srtFile.write(segment)
