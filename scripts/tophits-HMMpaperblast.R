library(tidyverse)
library(taxize)

files<-Sys.glob("papers/PaperBLAST/*.tsv")

captain_files <- files[grepl("YR",files)]
captain_files <- files[!grepl("tophits",captain_files)]

captain_results<-map_df(captain_files,~{
  read_tsv(.x, show_col_types = FALSE) %>%
    mutate(superfamily=gsub("papers/PaperBLAST/YRsuperfams.|.tsv","",.x)) %>%
    # separate(evidence, into=c("pident","coverage","bitscore"), sep=",") %>%
    # mutate(across(c(pident,coverage,bitscore),~trimws(.))) %>%
    rowwise() %>%
    mutate(palign=str_extract(evidence, "\\(\\d+\\.\\d+%\\)"),
      pcoverage=str_extract(evidence, "\\b\\d+\\.\\d+%\\b"),
      superfam=str_extract(evidence, "\\bsuperfam\\d+(?:-\\d+)?\\b"),
      bitscore=as.numeric(str_extract(evidence, "\\b\\d+\\.\\d+\\b")),
      lineage=(taxize::gnr_resolve(sci=species,best_match_only=TRUE,resolve_once=TRUE,fields="all") %>% pull(classification_path)))
})

top_captain_results<-captain_results %>% slice_max(order_by=bitscore,by=gene_id)

write_tsv(top_captain_results,"papers/PaperBLAST/YRsuperfams.tophits.tsv")
