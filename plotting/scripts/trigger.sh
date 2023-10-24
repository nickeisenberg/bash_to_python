#!/bin/bash

monitor_folder() {
    local DIR_PATH=""

    while [[ $# -gt 0 ]]; do
        key="$1"

        case $key in
            --folder)
            DIR_PATH="$2"
            shift # past argument
            shift # past value
            ;;
            *)
            echo "Unknown argument: $1"
            return 1
            ;;
        esac
    done

    if [[ -z "$DIR_PATH" ]]; then
        echo "Please specify a folder using the --folder parameter."
        return 1
    fi

    inotifywait -m "$DIR_PATH" -e create -e moved_to |
        while read path action file; do
            if [[ "$file" =~ .*\.png$ ]]; then
                xdg-open "$path/$file" &
            fi
        done
}

monitor_folder "$@"

