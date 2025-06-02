import os
import requests
from pathlib import Path
import xml.etree.ElementTree as ET

from nucleotide_query.api.genome.constants import URL, HEADERS, PARAMS

class GenomeReference:

    name: str
    sequence: str
    sequence_length: int

    @staticmethod
    def get_xml_path() -> str:
        cur_absolute_dir = Path(__file__).resolve().parent
        file_path = os.path.join(cur_absolute_dir, "data", "reference.xml")

        return file_path

    @classmethod
    def save_xml(cls, xml: bytes) -> None:
        output_path = cls.get_xml_path()

        # relatively small data we are requesting and saving
        # no streaming or async write needed
        with open(output_path, "wb") as f:
            f.write(xml)

    @classmethod
    def parse_xml(cls, xml: bytes) -> None:
        prefix = "TSeq"
        root = ET.fromstring(xml)
        cls.name = root.find(f"{prefix}/{prefix}_orgname").text
        cls.sequence_length = int(root.find(f"{prefix}/{prefix}_length").text)
        cls.sequence = root.find(f"{prefix}/{prefix}_sequence").text


    @classmethod
    def remote_query(cls) -> None:
        response = requests.get(URL, headers=HEADERS, params=PARAMS)

        # we check for valid responses with XML data, and save XML data locally
        response.raise_for_status()
        assert "xml" in response.headers.get("Content-Type", "").lower()
        cls.save_xml(response.content)

        # parse xml
        cls.parse_xml(response.content)












