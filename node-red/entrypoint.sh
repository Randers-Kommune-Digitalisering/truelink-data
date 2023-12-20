#!/bin/bash

trap stop SIGINT SIGTERM

function stop() {
        kill $CHILD_PID
        wait $CHILD_PID
}

# Decode base64 key data and write it to shh key file in SFTP module path
echo "$SSH_KEY" | base64 -d > "$SFTP_MODULE_PATH/$SFTP_SSH_KEY_FILE"

/usr/local/bin/node $NODE_OPTIONS node_modules/node-red/red.js --userDir /data $FLOWS "${@}" &

CHILD_PID="$!"

wait "${CHILD_PID}"