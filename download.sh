#!/bin/bash

# Set the dataset URL
DATASET_URL="https://zenodo.org/record/6420886/files/dataset.zip?download=1"

if [ ! -d "data" ]; then
  mkdir data
fi

# install aria2
function install_aria2() {
  if command -v apt-get > /dev/null; then
    sudo apt-get install aria2
  elif command -v yum > /dev/null; then
    sudo yum install aria2
  elif command -v dnf > /dev/null; then
    sudo dnf install aria2
  elif command -v pacman > /dev/null; then
    sudo pacman -S aria2
  else
    echo "Could not find a package manager. Please install aria2 manually."
    exit 1
  fi
}

# install aria2 if not installed 
if ! command -v aria2c > /dev/null; then
  read -p "aria2 is not installed. Do you want to install it using your package manager? [Y/n] " response
  if [[ $response =~ ^([yY][eE][sS]|[yY])$ ]]; then
    install_aria2
  else
fi


# Check if aria2 is installed
if command -v aria2c > /dev/null; then
  # Use aria2 to download the dataset
  aria2c -d data -o dataset.zip $DATASET_URL
else if command -v wget > /dev/null; then
  # Use wget to download the dataset
  wget -O data/dataset.zip $DATASET_URL
else if command -v curl > /dev/null; then
  # Use curl to download the dataset
  curl -L $DATASET_URL -o data/dataset.zip
else
  echo "aria2, wget, and curl are not installed. Please install one of these tools and try again."
  exit 1
fi

# Extract the dataset into the v1 directory
mkdir data -p
unzip data/dataset.zip -d data/temp
mv data/temp/dataset data/v1
rm -rf data/temp
rm data/dataset.zip
