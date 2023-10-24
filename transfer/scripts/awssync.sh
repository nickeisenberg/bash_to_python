#! /bin/bash

awssync() {

  local source_dir=""
  local save_dir=""
  local profile=""
  
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --source-dir)
        source_dir="$2"
        shift 2
        ;;
      --save-dir)
        save_dir="$2"
        shift 2
        ;;
      --profile)
        profile="$2"
        shift 2
        ;;
      *)
        echo "Invalid argument: $1"
        exit 1
        ;;
    esac
  done

  aws s3 sync $source_dir $save_dir \
    --profile $profile
}

awssync "$@"
