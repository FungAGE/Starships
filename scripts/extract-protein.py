import argparse
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from BCBio import GFF


def extract_protein_sequences(gff_file, fasta_file, output_fasta):
    # Parse the GFF file using BCBio's GFF parser
    with open(gff_file) as gff_handle:
        gff_records = list(GFF.parse(gff_handle))

    # Parse the FASTA file
    fasta_records = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta"))

    # Create a list to store protein sequences
    protein_sequences = []

    # Iterate through GFF entries
    for gff_record in gff_records:
        if "features" in gff_record and gff_record["features"]:
            for feature in gff_record["features"]:
                if feature["type"] == "CDS":
                    # Extract the protein sequence from the corresponding FASTA record
                    protein_sequence = fasta_records[
                        feature.qualifiers["ID"][0]
                    ].seq.translate()
                    # Create a SeqRecord for the protein sequence
                    protein_record = SeqRecord(
                        protein_sequence,
                        id=feature.qualifiers["ID"][0],
                        description=feature.qualifiers.get(
                            "product", ["Unknown product"]
                        )[0],
                    )
                    protein_sequences.append(protein_record)

    # Write the protein sequences to a new FASTA file
    SeqIO.write(protein_sequences, output_fasta, "fasta")


parser = argparse.ArgumentParser(description="Extract protein sequences from GFF file")
parser.add_argument("-g", "--gff", help='"-" for stdin', required=True)
parser.add_argument("-f", "--fasta", required=True)
parser.add_argument("-o", "--output", required=True)
args = parser.parse_args()

extract_protein_sequences(args.gff, args.fasta, args.output)
