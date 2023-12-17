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

    declare -A FILE_HASHES

    # Populate initial hashes
    for file in "$DIR_PATH"/*.png; do
        [[ -e "$file" ]] || continue
        FILE_HASHES["$file"]=$(md5sum "$file" | cut -d ' ' -f 1)
    done

    inotifywait -m "$DIR_PATH" -e create -e moved_to -e modify |
        while read path action file; do
            full_path="$path/$file"
            if [[ "$file" =~ .*\.png$ ]]; then
                current_hash=$(md5sum "$full_path" | cut -d ' ' -f 1)

                # If the file is modified and its hash is different than before
                if [[ $action == "MODIFY" && ${FILE_HASHES["$full_path"]} != "$current_hash" ]]; then
                    xdg-open "$full_path" &
                    FILE_HASHES["$full_path"]="$current_hash"
                # If the file is newly created or moved in
                elif [[ $action == "CREATE" || $action == "MOVED_TO" ]]; then
                    xdg-open "$full_path" &
                    FILE_HASHES["$full_path"]="$current_hash"
                fi
            fi
        done
}

monitor_folder "$@"

