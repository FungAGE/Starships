library(tidyverse)

starships<-read_tsv("Starships.withtaxa.tsv",col_names=c("Family","Species","Strain","Code","Navis","Size","DR","aTIR","Target","Spok","ARS","Other","HGT","taxID","taxRank","names","ranks"),show_col_types = FALSE) %>% 
  separate_rows(ranks,names,sep=";") %>%
  pivot_wider(id_cols=everything(),names_from=ranks,values_from=names,values_fn=function(x) x[1])
  # values_fn=function(x) paste0(unique(x),collapse="; "))

starships %>%
  select(-c(`no rank`,`NA`:section)) %>%
  mutate(across(superkingdom:genus,~replace_na(.,"Unknown"))) %>%
  write_csv(file="Starships.fulltaxa.csv")

