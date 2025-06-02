import os
import requests
from pathlib import Path
import xml.etree.ElementTree as ET

from nucleotide_query.api.genome.constants import URL, HEADERS, PARAMS


# todo maybe change file saving to DB

class GenomeReference:

    name: str = None
    sequence: str = None
    sequence_length: int = None

    @staticmethod
    def _get_xml_path() -> str:
        """
        Provide a consistent path for xml file.
        :return: a string representing the path that points to the reference xml file
        """
        cur_absolute_dir = Path(__file__).resolve().parent
        file_path = os.path.join(cur_absolute_dir, "data", "reference.xml")

        return file_path

    @classmethod
    def _save_xml(cls, xml: bytes) -> None:
        """
        Write the xml file to a pre-defined path.
        :param xml: byte data from an HTTP request
        """
        output_path = cls._get_xml_path()

        # relatively small data we are requesting and saving
        # no streaming or async write needed
        with open(output_path, "wb") as f:
            f.write(xml)

    @classmethod
    def _parse_xml(cls, xml: bytes) -> None:
        """
        Parse xml data and populate class variables for reference
        :param xml: byte data either read from a local file or from an HTTP request
        """
        prefix = "TSeq"
        root = ET.fromstring(xml)
        cls.name = root.find(f"{prefix}/{prefix}_orgname").text
        cls.sequence_length = int(root.find(f"{prefix}/{prefix}_length").text)
        cls.sequence = root.find(f"{prefix}/{prefix}_sequence").text


    @classmethod
    def _remote_query(cls) -> None:
        """
        Query NIH server for sequence. It saves queried data to a local file
        and pass data to parser

        :raises requests.exceptions.HTTPError: if encountering 400, 500 response
        :raises AssertionError: if the response is not of type application/xml or text/xml
        """
        response = requests.get(URL, headers=HEADERS, params=PARAMS)

        # we check for valid responses with XML data, and save XML data locally
        response.raise_for_status()
        assert "xml" in response.headers.get("Content-Type", "").lower()
        cls._save_xml(response.content)

        # parse xml
        cls._parse_xml(response.content)


    @classmethod
    def prepare(cls) -> None:
        """
        Load sequence data into memory from the local file, or start remote query if no such file exists
        """
        input_path = cls._get_xml_path()

        # try loading locally and fall back to
        # remote loading if needed
        try:
            with open(input_path, "rb") as f:
                contents = f.read()
                cls._parse_xml(contents)
        except FileNotFoundError:
            cls._remote_query()


    @classmethod
    def get(cls) -> str:
        """
        Get sequence string
        :return: sequence string
        """
        if cls.sequence is None:
            raise Exception("No sequence available")

        return cls.sequence













