import os
import requests
from pathlib import Path
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

    name: str
    sequence: str
    sequence_length: int

    @classmethod
    def parse_xml(cls, xml: bytes) -> None:
        pass


    @staticmethod
    def save_xml(xml: bytes) -> None:
        cur_absolute_dir = Path(__file__).resolve().parent
        output_path = os.path.join(cur_absolute_dir, "data", "reference.xml")

        # relatively small data we are requesting and saving
        # no streaming or async write needed
        with open(output_path, "wb") as f:
            f.write(xml)


    @classmethod
    def remote_query(cls) -> None:
        response = requests.get(URL, headers=HEADERS, params=PARAMS)

        # we check for valid responses with XML data, and save XML data locally
        response.raise_for_status()
        assert "xml" in response.headers.get("Content-Type", "").lower()
        cls.save_xml(response.content)

        # parse xml
        cls.parse_xml(response.content)












