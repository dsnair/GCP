#!/bin/bash

# Set-up project
echo -e "Setting-up your project\n"
gcloud init

# Create VM
echo -e "Setting-up your VM instance\n"
gcloud compute instances create instance-1 \
--image-project ubuntu-os-cloud \
--image-family ubuntu-1604-lts \
--scopes cloud-platform \
--network default

# Connect to VM
echo -e "Connecting to your VM instance\n"
gcloud compute ssh instance-1
