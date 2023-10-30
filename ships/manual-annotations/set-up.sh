#!/bin/bash

# TODO: store blastdb in SQL

BASEDIR=/home/adrian/Systematics/Starship_Database/starbase/Starships/ships/manual-annotations
cd $BASEDIR || exit

# TODO: once tax info is available for mycodb set...
STARSHIPS=/home/adrian/Systematics/Starship_Database/starbase/SQL/data/fna/ships/manual-annotations
# split fasta up
rm -f $STARSHIPS/Starships.part*

seqkit split -f -i Starships.fa -O $STARSHIPS

# fill in taxonomic information
tail -n +2 Starships.csv | tr "," "\t" | /usr/local/bin/taxonkit name2taxid -i 2 -r > Starships.withtaxaids.tsv

# FIXME: have to manually add missing taxids here

cat Starships.withtaxaids.tsv | /usr/local/bin/taxonkit lineage -i 14 -R > Starships.withtaxa.tsv

# creates Starships.fulltaxa.csv
#TODO: replace spaces and other characters (i.e. parentheses) in species names
# Rscript format_taxonomy.R
