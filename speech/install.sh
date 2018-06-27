#!/bin/bash

echo -e "Installing FFmpeg"
sudo apt-get install ffmpeg

echo -e "Installing pip"
sudo apt-get install python-pip python-dev build-essential
sudo pip install --upgrade pip

echo -e "Installing Speech API"
sudo pip install google-cloud-speech==0.27.1

echo -e "Installing gcsfuse"
sudo apt-get install lsb-release
export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install gcsfuse

echo -e "Checking installations"
ffmpeg -version
pip --version
gcsfuse --version
