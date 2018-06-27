#!/usr/bin/env python

# Reference: https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/speech/cloud-client/transcribe_async.py


import sys
import time
import os
import re
import subprocess

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


def transcribe_audio(gs_path):
    """ Transcribe an audio file to text """
    client = speech.SpeechClient()  # create an instance of client
    audio = types.RecognitionAudio(uri = gs_path)
    config = types.RecognitionConfig(
        encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code = "en-US")
    operation = client.long_running_recognize(config, audio)

    # Wait until the full audio file is read
    while not operation.done():
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(10)

    audio_text = ""
    alternatives = operation.result().results[0].alternatives
    for alternative in alternatives:
    #   audio_text += alternative.transcript.encode("utf-8")
        print('Transcript: {}'.format(alternative.transcript))

    # return audio_text


if __name__ == "__main__":
    gs_path = str(sys.argv[1])              # gs:// path for audio file stored on the cloud
    gs_bucket = os.path.split(gs_path)[0]   # GCS bucket name where audio file resides
    audio_file = os.path.split(gs_path)[1]  # audio file name
    audio_name = audio_file.split(".")[0]   # audio file name without the extension

    print("\nTranscribing audio:")
    transcribe_audio(gs_path)

    # concat_text = ""
    # for files in os.listdir("."):
    #     if files.endswith(".wav"):
    #         audio_text = transcribe_audio(gs_bucket+"/"+files)
    #         concat_text = concat_text + " " + audio_text
    #
    # with open("./"+audio_name+".txt", "w") as text_file:
    #     text_file.write(concat_text)

    print("\nFinished transcribing audio.")
