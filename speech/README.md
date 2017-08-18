# README

## Project Summary

In this tutorial, we'll learn how to use the [Google Cloud Speech API](https://cloud.google.com/speech/) to transcribe an audio file. The trickiest part of this API is converting your audio data into the correct format, which we'll do using [FFmpeg](https://www.ffmpeg.org/).

## Data

[YouTube Audio Library](https://www.youtube.com/audiolibrary/music) has a number of public domain audio files. The audio file transcribed in this tutorial (`John_F_Kennedy_Inaugural_Speech_January_20_1961.mp3`) was downloaded from this library (by searching "speech" in the search box).

### Data Size Limitations

**Audio longer than 1 minute must reside on Google Cloud Storage** (GCS) and **audio up to 80 minutes duration can be processed at a time** [(usage limit)](https://cloud.google.com/speech/limits).

Since most audio files would be longer than 1 minute, we'll skip the part where files could be transcribed locally on your laptop and instead we'll learn how to transcribe files on Google Cloud Storage.

## Requirements

### I. Google Cloud Platform (GCP) credentials
   1. If you haven't already, you may sign-up for the [free GCP trial credit](https://cloud.google.com/free/docs/frequently-asked-questions)
   * [Set up your project](https://cloud.google.com/speech/docs/getting-started#set_up_your_project) on GCP and enable the Speech API

### II. [Create a GCS bucket](https://cloud.google.com/storage/docs/quickstart-console#create_a_bucket)

### III. Install packages

[Start your cloud shell](https://cloud.google.com/shell/docs/quickstart#start_cloud_shell) and let's install the following packages. Note that none of these packages will persist once you log-out of this shell session. If you want [persistence](https://cloud.google.com/shell/docs/features#persistent_disk_storage), then `cd /home`.

#### 1. Install FFmpeg  
```shell
$ sudo apt-get install ffmpeg
```

#### 2. Install the Speech API Python library  
```shell
$ sudo pip install google-cloud-speech==0.27.1
```

#### 3. Install [gcsfuse](https://github.com/GoogleCloudPlatform/gcsfuse/blob/master/docs/installing.md)

gcsfuse mounts a directory on your cloud shell to a bucket on GCS. This allows the two directories on different machines to see each others content and be in sync when the directory contents change.

```shell
$ sudo apt-get install lsb-release
$ export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
$ echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
$ curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
$ sudo apt-get update
$ sudo apt-get install gcsfuse
```

Now let's mount a local directory (named `local_bucket`) on your cloud shell to your GCS bucket.

```shell
$ mkdir local_bucket
$ gcsfuse your-bucket-name local_bucket
$ cd local_bucket/
$ ls
```

### IV. Clone this Repo
```shell
$ git clone https://github.com/dsnair/GCP.git
$ cd speech
$ ls
```
Note that the contents of this repo are now visible in `your-bucket-name` on GCS.

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
* [Delete your bucket](https://cloud.google.com/storage/docs/quickstart-console#clean-up) to avoid incurring charges to your account.

## What's Next?

If you need more computing power, consider starting a VM instance on GCP.  It can be done in two simple steps:
   1. [Create a VM instance](https://cloud.google.com/compute/docs/quickstart-linux#create_a_virtual_machine_instance)
       * Select **Ubuntu** under 'Boot disk' for all the above installation commands to work
       * '**Allow full access to all Cloud APIs**' under 'Access scopes'
   2. [Connect to your VM instance](https://cloud.google.com/compute/docs/quickstart-linux#connect_to_your_instance)

(`vm-setup.sh` creates a VM instance named `instance-1` with the configurations stated above. Execute this bash script as follows:
```shell
$ chmod +x vm-setup.sh
$ ./vm-setup.sh
```
)

The cloud shell comes pre-installed with pip and git. However, you'd have to install pip yourself on a VM instance:
```shell
$ sudo apt-get install python-pip python-dev build-essential
$ sudo pip install --upgrade pip
$ sudo apt-get install git
```

Again, files stored and packages installed in the **HOME** directory on your VM instance will persist.

Don't forget to [delete your VM instance](https://cloud.google.com/compute/docs/quickstart-linux#clean-up) after you're done to avoid incurring charges to your GCP account.

## Reference

1. [Speech API GitHub repo](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/speech/cloud-client)
2. [Intro to Audio Encoding](https://cloud.google.com/speech/docs/encoding)