#!/bin/bash

IN_DIR="/rsgrps/laurameredith/data/LEO_iTag/water/splitfiles/split1"
OUT_DIR="/rsgrps/laurameredith/data/LEO_iTag/water/splitfiles/fastq_info1"

if [[ ! -d "$OUT_DIR" ]]; then
    mkdir -p "$OUT_DIR"
fi

FASTQ_FILES=$(mktemp)
find "$IN_DIR" -type f -name \*.fastq > "$FASTQ_FILES"

i=0
while read -r FASTQ; do
    i=$((i+1))
    BASENAME=$(basename "$FASTQ")
    printf "%3d: %s\\n" $i $BASENAME
    usearch -fastx_info "$FASTQ" -output "$OUT_DIR/$BASENAME" 1>/dev/null 2>&1
done < "$FASTQ_FILES"

echo "Done."
