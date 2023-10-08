#!/bin/bash

CSV_PATH="metadata/dataset.csv"
TGT_DIR="chad_dataset/"
EXT=".mp3"
SR=16000

python3.9 src/main.py \
    --csv-path "$CSV_PATH" \
    --tgt-dir "$TGT_DIR" \
    --extension "$EXT" \
    --download-hf-dataset \
    --save-fragments_audios \
    --save-full_audios \
    --save-metadata \
    --sr "$SR" \
    --mono