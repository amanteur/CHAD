#!/bin/bash

CSV_PATH="metadata/dataset.csv"
TGT_DIR="chad_dataset/"
EXT=".mp3"
SAVE_FRAGMENTS_AUDIOS="True"
SAVE_FULL_AUDIOS="True"
SAVE_METADATA="True"
N_PROCESSES=8
SR=16000

python3.9 src/main.py \
    --csv_path "$CSV_PATH" \
    --tgt_dir "$TGT_DIR" \
    --extension "$EXT" \
    --save_fragments_audios "$SAVE_FRAGMENTS_AUDIOS" \
    --save_full_audios "$SAVE_FULL_AUDIOS" \
    --save_metadata "$SAVE_METADATA" \
    --n_processes "$N_PROCESSES" \
    --sr "$SR" \
    --mono