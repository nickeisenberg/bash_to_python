#! /bin/bash

PORT="22"
SOURCE_PATH="/home/nicholas/GitRepos/pyaws/test/scp/move"
SAVE_PATH="/home/ubuntu/movedir"
USER="ubuntu"
IP="50.18.80.35"

# echo $PORT
# echo $SOURCE_PATH
# echo $SAVE_PATH
# echo $USER
# echo $IP

# scp -v -r -P $PORT $SOURCE_PATH $USER@$IP:$SAVE_PATH

scp -v -r -P $PORT $SOURCE_PATH $USER@$IP:$SAVE_PATH
