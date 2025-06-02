import requests
import xml.etree.ElementTree as ET

from nucleotide_query.api.genome.constants import URL, HEADERS, PARAMS, SEQUENCE_DATA_FIELDS
from nucleotide_query.api.models import Sequence


class GenomeReference:

    name: str = None
    sequence: str = None
    sequence_length: int = None

    @staticmethod
    def _get_query_data() -> dict:
        """
        Provides keys for querying the Sequence model based on NIH API query

        :return: dictionary with fields, in combination should be unique to Sequence model
        """
        query_data = {
            "nih_db": PARAMS['db'],
            "nih_id": PARAMS['id'],
            "type": PARAMS['rettype'],
        }

        return query_data

    @classmethod
    def _populate_variables(cls, sequence_data) -> None:
        """
        Populates class variables for in-memory use later

        :param sequence_data: a dictionary with at least 'orgname', 'length', and 'sequence' fields
        """

        # populate to singleton instance's variables
        cls.name = sequence_data['orgname']
        cls.sequence_length = sequence_data['length']
        cls.sequence = sequence_data['sequence']

    @classmethod
    def _parse_and_save_sequence_data(cls, xml: bytes) -> None:
        """
        Parses XML data and save to database

        :param xml: byte data of XML, fetched from NIH API
        """

        prefix = "TSeq"
        root = ET.fromstring(xml)

        # query data are also fields of sequence data
        sequence_data = cls._get_query_data()

        # load data according to pre-defined fields
        for field in SEQUENCE_DATA_FIELDS:
            raw_text = root.find(f"{prefix}/{prefix}_{field}").text
            if field == 'length':
                sequence_data[field] = int(raw_text)
            else:
                sequence_data[field] = raw_text

        # save to database
        Sequence.objects.create(**sequence_data)

        # populate to singleton instance's variables
        cls._populate_variables(sequence_data)


    @classmethod
    def _load_from_db(cls) -> None:
        """
        Loads sequence data from database into memory
        """

        query_data = cls._get_query_data()

        # query data with the unique combination
        sequence_data = Sequence.objects.values('orgname', 'length', 'sequence').get(**query_data)

        # populate to singleton instance's variables
        cls._populate_variables(sequence_data)

    @classmethod
    def _remote_query(cls) -> None:
        """
        Query NIH server for sequence. It passed data for parsing and saving to database

        :raises requests.exceptions.HTTPError: if encountering 400, 500 response
        :raises AssertionError: if the response is not of type application/xml or text/xml
        """
        response = requests.get(URL, headers=HEADERS, params=PARAMS)

        # we check for valid responses with XML data, and start data processing
        response.raise_for_status()
        assert "xml" in response.headers.get("Content-Type", "").lower()
        cls._parse_and_save_sequence_data(response.content)


    @classmethod
    def prepare(cls) -> None:
        """
        Load sequence data into memory from the local DB, or start remote query if no such file exists
        """

        try:
            cls._load_from_db()
        except Sequence.DoesNotExist:
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













