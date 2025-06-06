#!/bin/bash

curl --location 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&rettype=fasta&retmode=xml&id=224589800' \
--header 'Accept: text/xml' \
-o 224589800.xml