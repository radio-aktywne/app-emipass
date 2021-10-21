#!/bin/sh

print_usage() {
    # Prints script usage

    cat <<EOF
Usage: $0 [-p PORT]
    -p, --port             port to listen on for audio streams (default: 10000)
EOF
}

port='10000'

while [ "$#" -gt 0 ]; do
    case "$1" in
    -p | --port)
        shift
        port="$1"
        ;;
    -h | --help)
        print_usage
        exit
        ;;
    esac
    shift
done

EMIPASS_SOURCE_PORT="$port" node main.js
