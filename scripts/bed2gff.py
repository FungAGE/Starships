import argparse
import os
import pandas as pd

# Columns in a gff file:
# "seqid", "source", "type", "start", "end", "score", "strand", "phase", "attributes"

# Create a command-line argument parser
parser = argparse.ArgumentParser(description="Process TSV and BED files")

parser.add_argument(
    "-b", "--bed", dest="bed_file", help="Path to the BED file", required=True
)
parser.add_argument(
    "-f",
    "--features",
    dest="feature_file",
    help="Path to the feature file",
    required=True,
)

parser.add_argument(
    "-o",
    "--output",
    dest="output_directory",
    help="Output directory path",
    required=True,
)

# Parse the command-line arguments
args = parser.parse_args()

# make coordinates in gff relative to the element, rather than the chr. Use columns 4 and 5 in `mycodb.final.starships.feat` to correct. and remember, gff is 1-indexed
# Load the TSV file into a DataFrame
df = pd.read_csv(args.feature_file, sep="\t")

# Initialize a dictionary to store data on element lengths
begin_dict = {}
end_dict = {}
for index, row in df.iterrows():
    id_value = row["starshipID"]
    # Calculate the length of elements
    start = row["elementBegin"]
    end = row["elementEnd"]
    begin_dict[id_value] = start
    end_dict[id_value] = end

# Initialize a dictionary to store data for each ID
data_by_id = {}

with open(args.bed_file, "r") as bed_file:
    for line in bed_file:
        fields = line.strip().split("\t")
        contig = fields[0]
        name = fields[3]
        feature = fields[4]
        strand = fields[5]
        element = fields[6]  # 7th column with comma-separated items

        if feature == "flank" or feature == "insert":
            type = "region"
        else:
            type = "gene"
        score = "."
        phase = "."

        # don't parse split/nested elements
        while element not in (",", "|") not in element:
            start = abs(int(begin_dict[element]) - int(fields[1])) + 1
            end = abs(int(fields[2]) - int(fields[1])) + start

            output = f"{element}\tbed\t{type}\t{start}\t{end}\t{score}\t{strand}\t{phase}\tID=gene_{name};Description={element};parent={contig}"

            name_key = element

            # Check if the ID already exists in the dictionary
            if name_key in data_by_id:
                data_by_id[name_key].append(output)
            else:
                data_by_id[name_key] = [output]

# Create a directory to store the output files
# output_directory = args.bed_file.strip(".bed") + "_split"
os.makedirs(args.output_directory, exist_ok=True)

# Create separate GFF files for each ID
for name_key, data in data_by_id.items():
    output_file_name = f"{args.output_directory}/{name_key}.gff"
    # Create a list to store RNA/CDS entries for each gene
    rna_entries = []
    cds_entries = []

    with open(output_file_name, "w") as output_file:
        for line in data:
            output_file.write(line + "\n")

            # Extract gene start and end coordinates from the line
            fields = line.split("\t")
            if fields[2] == "gene":
                gene_start = int(fields[3])
                gene_end = int(fields[4])
                id = fields[8].split(";")[0]
                description = fields[8].split(";")[1]
                rna_id = id.replace("gene_", "rna_")
                rna_parent = id.replace("ID=", "parent=")
                cds_id = id.replace("gene_", "cds_")
                cds_parent = rna_id.replace("ID=", "parent=")

                # Create a RNA entry for the gene
                rna_entry = f"{fields[0]}\tbed\tmRNA\t{gene_start}\t{gene_end}\t{fields[5]}\t{fields[6]}\t.\t{rna_id};{description};{rna_parent}"
                rna_entries.append(rna_entry)

                # Create a CDS entry for the gene
                cds_entry = f"{fields[0]}\tbed\tCDS\t{gene_start}\t{gene_end}\t{fields[5]}\t{fields[6]}\t.\t{cds_id};{description};{cds_parent}"
                cds_entries.append(cds_entry)

    # Append CDS entries to the output GFF file
    # with open(output_file_name, "a") as output_file:
    #     for rna_entry in rna_entries:
    #         output_file.write(rna_entry + "\n")
    #     for cds_entry in cds_entries:
    #         output_file.write(cds_entry + "\n")
