#! /bin/bash

scp() {
    # Default values
    local PORT=22
    local SOURCE_PATH=""
    local SAVE_PATH=""
    local USER=""
    local IP=""

    # Parse arguments
    while [[ $# -gt 0 ]]
    do
    key="$1"

    case $key in
        --port)
        PORT="$2"
        shift # past argument
        shift # past value
        ;;
        --source-path)
        SOURCE_PATH="$2"
        shift # past argument
        shift # past value
        ;;
        --save-path)
        SAVE_PATH="$2"
        shift # past argument
        shift # past value
        ;;
        --user)
        USER="$2"
        shift # past argument
        shift # past value
        ;;
        --ip)
        IP="$2"
        shift # past argument
        shift # past value
        ;;
        *)
        echo "Unknown argument: $1"
        return 1
        ;;
    esac
    done

    # Check if all required parameters are set
    if [[ -z "$SOURCE_PATH" || -z "$SAVE_PATH" || -z "$USER" || -z "$IP" ]]; then
        echo "Required parameters missing."
        return 1
    fi

    # Run scp
    scp -P "$PORT" "$SOURCE_PATH" "${USER}@${IP}:${SAVE_PATH}"
}

scp "$@"
