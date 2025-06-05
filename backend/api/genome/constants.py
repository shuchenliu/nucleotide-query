URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
PARAMS = {
    "db": "nucleotide",
    "id": "30271926",
    "rettype": "fasta",
    "retmode": "xml",
}

# emphasize expected data type
HEADERS = {"accept": "text/xml"}

SEQUENCE_DATA_FIELDS = [
    'seqtype',
    'accver',
    'taxid',
    'orgname',
    'defline',
    'length',
    'sequence'
]