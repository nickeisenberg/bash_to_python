#! /bin/bash

PORT="22"

# for my mac
SOURCE_PATH="/Users/nickeisenberg/GitRepos/sshtools/tests/transfer/move"

# for my linux
SOURCE_PATH="/home/nicholas/GitRepos/sshtools_project/sshtools/tests/transfer/move"

SAVE_PATH="/ebs0/nick/Tmp/sshtools_test"
USER="nick"
IP="54.183.226.197"

/Users/nickeisenberg/GitRepos/sshtools/src/sshtools/transfer/scripts/scp.sh --port $PORT --source-path $SOURCE_PATH --save-path $SAVE_PATH --user $USER --ip $IP
