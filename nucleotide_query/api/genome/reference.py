import requests
import xml.etree.ElementTree as ET

URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
PARAMS = {
    "db": "nucleotide",
    "id": "30271926",
    "rettype": "fasta",
    "retmode": "xml",
}

# emphasize expected data type
HEADERS = {"accept": "text/xml"}

class GenomeReference:

    @staticmethod
    def parse_xml(xml):
        pass


    @staticmethod
    def remote_query():
        response = requests.get(URL, headers=HEADERS, params=PARAMS)

        # we check for valid responses with XML data, and save XML data locally
        response.raise_for_status()
        assert "xml" in response.headers.get("Content-Type", "").lower()

        # relatively small data we are requesting and saving, no streaming needed
        with open("reference.xml", "wb") as f:
            f.write(response.content)











