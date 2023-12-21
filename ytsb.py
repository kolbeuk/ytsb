#!/usr/bin/env python
# coding: utf-8

from pytube import YouTube
import concurrent.futures
import sys
import os
import whisper
import datetime

def download_and_transcribe(urls):
    try:
        yt = YouTube(urls)
        yt = YouTube(
            urls,
            use_oauth=False,
            allow_oauth_cache=True
        )
        stream = yt.streams.get_lowest_resolution()
        print(f"Downloading video: {yt.title}")
        stream.download()
        print(f"Downloaded video: {yt.title}")
        return stream.default_filename
            
    except Exception as e:
        print(f"Error initializing YouTube object: {e}")
        return None

def transcribe_video(filename):
    try:
        # Load the Whisper model
        model = whisper.load_model("tiny")
        print("Whisper model loaded.")

        print(f"Transcribing video: {filename}")
        result = model.transcribe(filename, fp16=False, verbose=None)
        
        # Get the current date and time
        current_datetime = datetime.datetime.now().strftime("%m-%d_%H-%M")

        # Modify the transcript filename
        transcript_filename = f"{current_datetime}_{filename}.txt".replace('/', '_').replace('\\', '_')
        
        # Write the transcription to a file
        with open(transcript_filename, 'w') as file:
            file.write(result['text'])
        
        print(f"Transcription saved to '{transcript_filename}'")
        
        # Attempt to delete the file
        os.remove(filename)
        
    except Exception as e:
        print(f"Error during transcription: {e}")
        
def main(urls):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Download videos and transcribe concurrently
        futures = []
        for url in urls:
            # Download and get the filename
            filename = download_and_transcribe(url)
            if filename:
                # Submit the filename to the transcribe_video function
                futures.append(executor.submit(transcribe_video, filename))

        # Wait for all tasks to complete
        concurrent.futures.wait(futures)
    
if __name__ == "__main__":
    # Assuming file paths are passed as separate command-line arguments
    urls = sys.argv[1:]
    main(urls)
