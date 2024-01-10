# #TODO:

- [x] prepare `.mtdb`
  - only from "high confidence" set? `mycodb.final.restrict.fog6.d600000.m2`
  - pulling metadata from `mycodb.final.restrict.fog6.d600000.m2.regions.txt`
    - ~~[ ] get taxonomic information~~
      - ~~match headers from `mycodb.final.starships.fna` to column `memberID` for each starship~~
        - not going to work because there are custom `memberID`s here for unpublished assemblies
- [x] make gffs for each starship from the bed file

- [ ] add gene sequences
  - should match up with gff coordinates

# Notes

- the `.mtdb` file must contain the paths to the `.fna`, `.faa`, and `.gffs` files
