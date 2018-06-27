#!/usr/bin/env python

import os
import subprocess
import sys
import re


def format_audio(local_audio):
    # Find audio duration
    duration = ["ffprobe",
                # suppress all but error messages
                "-v", "error",
                # duration in seconds.microseconds
                "-show_entries", "format=duration",
                # set print format
                "-of", "default=noprint_wrappers=1:nokey=1",
                local_audio]
    proc = subprocess.Popen(duration, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    seconds = float(proc.communicate()[0])

    # Format audio
    print("\nFormatting audio:")
    # if audio > 4800 seconds (80 minutes), chunk it
    if (seconds > 4800):
        chunk = ["ffmpeg",
                 # suppress all but error messages
                 "-loglevel", "panic",
                 # input audio file path
                 "-i", local_audio,
                 # linear16 audio encoding
                 "-acodec", "pcm_s16le",
                 # mono channel
                 "-ac", "1",
                 "-f", "segment",
                 # chunk at every 4800 seconds interval
                 "-segment_time", "4800",
                 local_bucket+"/"+file_name+"%d.wav"]
        subprocess.call(chunk)
    # skip chunking if audio < 4800 seconds
    else:
        extract = ["ffmpeg",
                   "-loglevel", "panic",
                   "-i", local_audio,
                   "-acodec", "pcm_s16le",
                   "-ac", "1",
                   local_bucket+"/"+file_name+".wav"]
        subprocess.call(extract)
    print("\nFinished extracting audio.")


if __name__ == "__main__":
    # gs:// path for audio file stored on GCS
    gs_path = str(sys.argv[1])
    # bucket name where audio file resides on GCS
    gs_bucket = os.path.split(gs_path)[0]
    # local path on cloud shell for audio file
    local_bucket = re.split("://", gs_bucket)[1]
    # audio file name
    audio_name = os.path.split(gs_path)[1]
    # audio file name without the extension
    file_name = audio_name.split(".")[0]

    format_audio(local_bucket+"/"+audio_name)
