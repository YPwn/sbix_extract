#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 TTF_EXTRACTED_DIR"
    exit 0
fi

if [ -x "$(command -v sbix_emjc_decode)" ]; then
    decoder="sbix_emjc_decode"
elif [ -f "sbix_emjc_decode" ]; then
    decoder="./sbix_emjc_decode"
else
    echo "Error: Decoder not found!"
    exit 1
fi

for f in $(find "$1" -type f -name *.emjc); do
    "$decoder" "$f" | grep -v Dimensions
done

