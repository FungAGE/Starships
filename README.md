# Database of Starship Elements and Starship-associated Genes

## Structure of this Repo

- `ships`: full Starship sequences
- `captain`:`tyr` gene
- `cargo`: `nlr`, `fre`, `plp`, and `duf3723` genes

Each folder contains:

- databases for BLAST and `.hmm` for `hmmersearch`, including:
  - a nucleotide database for Starship sequences: `ships/fna/blastdb/concatenated.fa`
  - individual nucleotide/protein databases for each `captain` and `cargo` gene

# TODO

- [ ] extract `captain`/`cargo` genes from `manual-annotations` ships
  - [ ] add `manual-annotations` to `hmm` models
  - [ ] update `blastdb`'s
