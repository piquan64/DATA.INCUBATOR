IN_DIR="/rsgrps/laurameredith/data/LEO_iTag/water/splitfiles/split1"
OUT_DIR="/rsgrps/laurameredith/data/LEO_iTag/water/splitfiles/merge1"

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
    usearch -fastq_mergepairs "$FASTQ" -fastqout "$OUT_DIR/$BASENAME" -relabel @ -fastq_maxdiffs 10 -fastq_pctid 80
done < "$FASTQ_FILES"

echo "Done."
