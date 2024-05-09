#!/bin/bash
out_dir=papers/PaperBLAST
mkdir -p $out_dir

# run through the separate gene models for each captain family
awk -v RS="//" '{print $0 > ("YRsuperfams." NR ".hmm")}' captain/tyr/hmm/YRsuperfams.p1-512.hmm
mv YRsuperfams.*.hmm $out_dir/

captain_hmm_files=$(find $out_dir/ -name "YRsuperfams.*.hmm" -type f -size +100b)

for captain_hmm_file in $captain_hmm_files; do
  out_file=$(basename "$captain_hmm_file" .hmm)
  printf "Processing %s ..." "$out_file"
  # make sure the file ends with "//"
  sed -i '1{/^$/d}' "$captain_hmm_file" 
  echo "//" >> "$captain_hmm_file"
  python scripts/HMMpaperblast.py "$captain_hmm_file" "$out_dir"/"$out_file".tsv
  rm -f "$captain_hmm_file"
done

# now combine results and find the best hit for each hit?
Rscript scripts/tophits-HMMpaperblast.R

# # run gene models for cargo genes
# cargo_hmm_files=$(find cargo/*/hmm -name "*.hmm")
# for cargo_hmm_file in $cargo_hmm_files; do
#   out_file=$(basename "$cargo_hmm_file" .hmm)
#   python scripts/HMMpaperblast.py "$cargo_hmm_file" "$out_dir"/"$out_file".tsv
# done