# README

## Project Summary

In this tutorial, we'll learn how to use the [Google Cloud Speech API](https://cloud.google.com/speech/) to transcribe an audio file. The trickiest part of this API is converting your audio data into the correct format, which we'll do using [FFmpeg](https://www.ffmpeg.org/).

## Data

[YouTube Audio Library](https://www.youtube.com/audiolibrary/music) has a number of public domain audio files. The audio file transcribed in this tutorial (`John_F_Kennedy_Inaugural_Speech_January_20_1961.mp3`) was downloaded from this library.

### Data Size Limitations

**Audio longer than 1 minute must reside on Google Cloud Storage** (GCS) and **audio up to 80 minutes duration can be processed at a time** [(usage limit)](https://cloud.google.com/speech/limits).

Since most audio files would be longer than 1 minute, we'll skip the part where files could be transcribed locally on your laptop and instead we'll learn how to transcribe files on GCS.

## Requirements

### I. Google Cloud Platform (GCP) credentials
   1. If you haven't already, you may sign-up for the [free GCP trial credit](https://cloud.google.com/free/docs/frequently-asked-questions)
   * [Set up your project](https://cloud.google.com/speech/docs/getting-started#set_up_your_project) on GCP

### II. GCS bucket
1. [Create a GCS bucket](https://cloud.google.com/storage/docs/quickstart-console#create_a_bucket)
2. [Upload](https://cloud.google.com/storage/docs/quickstart-console#upload_an_object_into_the_bucket) the JSON file for the service account key that you just created in the step above
3. Clone this repo on the [cloud shell](https://cloud.google.com/shell/docs/quickstart#start_cloud_shell):
```shell
$ git clone https://github.com/dsnair/GCP.git
$ cd speech
$ ls
```

### III. VM

On the cloud shell, run the `vm-setup.sh` script to create an Ubuntu-based VM instance named `instance-1`:
```shell
$ chmod +x vm-setup.sh
$ ./vm-setup.sh
```
OR

Do it manually on the Console:
1. [Create a VM instance](https://cloud.google.com/compute/docs/quickstart-linux#create_a_virtual_machine_instance)
    * Select **Ubuntu** under 'Boot disk' for all the above installation commands to work
    * '**Allow full access to all Cloud APIs**' under 'Access scopes'
2. [Connect to your VM instance](https://cloud.google.com/compute/docs/quickstart-linux#connect_to_your_instance)

### IV. Install packages

1. Clone this repo on your VM (different from the cloud shell)
2. On your VM, run the `install.sh` script to install FFmpeg, the Speech API client for Python, and [gcsfuse](https://github.com/GoogleCloudPlatform/gcsfuse/blob/master/docs/installing.md):
```shell
$ chmod +x install.sh
$ ./install.sh
```

### V. Mount local directory

gcsfuse mounts a directory on your VM to a bucket on GCS. This allows the two directories on different machines to see each others content and be in sync when the directory contents change.

Now, let's mount a local directory named `local_bucket` on your VM to your GCS bucket.

```shell
$ mkdir local_bucket
$ gcsfuse your-bucket-name local_bucket
$ cd local_bucket/
$ ls
```

Set the environment variable to point to the service account key:
```shell
$ export GOOGLE_APPLICATION_CREDENTIALS=path_to/service_account_file.json
```

## Transcribe Audio file


```shell
$ python transcribe_audio.py gs://your-bucket-name/John_F_Kennedy_Inaugural_Speech_January_20_1961.mp3
```

**Output:** `transcribe_audio.py` formats the audio file to create .WAV file and outputs the audio transcription on your shell.

### Format Audio file

Here are the details on how the audio file is formatted using FFmpeg:

```shell
$ ffmpeg -i John_F_Kennedy_Inaugural_Speech_January_20_1961.mp3 -acodec pcm_s16le -ac 1 -f segment -segment_time 4800 John_F_Kennedy_Inaugural_Speech_January_20_1961_%d.wav
```
**Output:** The command line above creates `John_F_Kennedy_Inaugural_Speech_January_20_1961_0.wav` in `local_bucket`, which is also visible in `your-bucket-name`.

* `-i` takes an input audio file
* `-acodec pcm_s16le` sets linear16 audio encoding
* `-ac 1` sets mono channel
* `-segment_time 4800` chunks the input audio file at every 4800 seconds (80 minutes) and names each chunk filename_0.wav, filename_1.wav, etc.

## Clean-up

* Unmount your local directory
```shell
$ cd
$ fusermount -u local_bucket
```
* [Delete your bucket](https://cloud.google.com/storage/docs/quickstart-console#clean-up) to avoid incurring charges to your account
* [Delete your VM instance](https://cloud.google.com/compute/docs/quickstart-linux#clean-up)

## Reference

1. [Speech API GitHub repo](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/speech/cloud-client)
2. [Intro to Audio Encoding](https://cloud.google.com/speech/docs/encoding)
