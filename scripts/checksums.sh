#!/bin/bash

files="fna
faa"

genes="tyr
duf3723
fre
nlr
plp"

types="cargo
ships"

# generate checksum based on sequence
# ? strandedness ?
# ? adapting/adding information to headers ?

for file in $files; do
  for type in $types;   do
    if [[ $file == "fna" ]]; then
      sql_dir="SQL/data/$file/$type"
      find $sql_dir -type f \( -name "*.fa" -o -name "*.fna" \) | seqkit sum -j 4 - | sed 's/seqkit.v0.1_DLS_k0_|seqkit.v0.1_PLS_k0_//g' > "$sql_dir"/"$file".checksums.txt
    elif [[ $file == "faa" ]]; then
      for gene in $genes
        do
          repo_dir=$type/$gene
          sql_dir="SQL/data/$file/$type/$gene"
          mkdir -p "$sql_dir/mycodb"
          
          # skip because we've already done this
          if [[ $gene != "tyr" ]]; then
            # automate splitting of multifastas into separate fastas
            seqkit split -j 4 -f -i "$repo_dir"/*."$file" -O "$sql_dir/mycodb"
          fi

          # processing of checksums for all genes
          seqkit sum -j 4 "$sql_dir"/*/* | sed 's/seqkit.v0.1_DLS_k0_|seqkit.v0.1_PLS_k0_//g' > "$sql_dir"/"$file".checksums.txt
        done
    fi
  done
done

# remove empty files
find SQL/ -name "*.checksums.txt" -type f -empty -delete

CHECKSUMS=$(find SQL/ -name "*.checksums.txt")

# check for duplicates
for CHECKSUM in $CHECKSUMS; do
  DIR=$(basedir $CHECKSUM)
  # number of entries
  wc -l $DIR/$type.checksums.txt
  # number of unique entries
  cut -f 1 $DIR/$type.checksums.txt | sort | uniq | wc -l
done
