#!/usr/bin/env python
# coding: utf-8

from pytube import YouTube
import concurrent.futures
import sys
import whisper

def download_and_transcribe(url, model):
    yt = YouTube(url)
    stream = yt.streams.get_lowest_resolution()
    print(f"Downloading video: {yt.title}")
    stream.download()
    print(f"Downloaded video: {yt.title}")
        
    # Transcribe the video
    filename = stream.default_filename
    try:
        print(f"Transcribing video: {yt.title}")
        result = model.transcribe(filename, fp16=False, verbose=None)
        
        # Create a valid filename for the transcription
        transcript_filename = f"{yt.title}.txt".replace('/', '_').replace('\\', '_')
        
        # Write the transcription to a file
        with open(transcript_filename, 'w') as file:
            file.write(result['text'])
        
        print(f"Transcription saved to '{transcript_filename}'")
    except Exception as e:
        print(f"Error during transcription: {e}")


def main(urls):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_video, urls)

if __name__ == "__main__":
    # Assuming URLs are passed as separate command-line arguments
	
    urls = sys.argv[1:]
    
    # Load the Whisper model
    model = whisper.load_model("tiny")
    print("Whisper model loaded.")
    
    main(urls)
