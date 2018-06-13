IN_DIR="/rsgrps/laurameredith/data/LEO_iTag/water/splitfiles/split1"
OUT_DIR="/rsgrps/laurameredith/data/LEO_iTag/water/splitfiles/eestats1"

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
    usearch -fastq_eestats2 "$FASTQ" -output "$OUT_DIR/$BASENAME" -length_cutoffs 200,300,10 
done < "$FASTQ_FILES"

echo "Done."

