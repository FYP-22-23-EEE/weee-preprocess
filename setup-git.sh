#!/bin/bash

SSH_KEY_PATH="$PWD/.git-ssh/id_rsa"
USER_INFO_PATH="$PWD/.git-ssh/user_info"

# exit if above files are not found
if [ ! -f "$SSH_KEY_PATH" ] || [ ! -f "$USER_INFO_PATH" ]; then
    echo "SSH key or user info not found at $SSH_KEY_PATH or $USER_INFO_PATH"
    exit 1
fi

# Read user email and name from user_info file
USER_EMAIL=$(head -n 1 $USER_INFO_PATH)
USER_NAME=$(tail -n 1 $USER_INFO_PATH)

# Configure git with user email and name
git config --global user.email "$USER_EMAIL"
git config --global user.name "$USER_NAME"

# copy ssh key to ~/.ssh/id_rsa
cp $SSH_KEY_PATH ~/.ssh/id_rsa
chmod 600 ~/.ssh/id_rsa

# Add ssh key to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa

# Test the ssh connection to GitHub
ssh -T git@github.com

