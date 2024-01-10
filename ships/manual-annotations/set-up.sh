#!/bin/bash

# TODO: store blastdb in SQL

BASEDIR=ships/manual-annotations

# TODO: once tax info is available for mycodb set...
STARSHIPS=SQL/data/fna/ships/manual-annotations
# split fasta up
rm -f $STARSHIPS/Starships.part*

seqkit split -f -i $BASEDIR/Starships.fa -O $STARSHIPS

# fill in taxonomic information
tail -n +2 $BASEDIR/Starships.csv | tr "," "\t" | /usr/local/bin/taxonkit name2taxid -i 2 -r > $BASEDIR/Starships.withtaxaids.tsv

# FIXME: have to manually add missing taxids here

cat $BASEDIR/Starships.withtaxaids.tsv | /usr/local/bin/taxonkit lineage -i 14 -R > $BASEDIR/Starships.withtaxa.tsv

# creates Starships.fulltaxa.csv
#TODO: replace spaces and other characters (i.e. parentheses) in species names
Rscript scripts/format_taxonomy.R
