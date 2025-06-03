import requests
import xml.etree.ElementTree as ET

from api.genome.constants import URL, HEADERS, PARAMS, SEQUENCE_DATA_FIELDS
from api.models import Sequence


class GenomeReference:

    sequence_id = None
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
        cls.sequence_id = sequence_data['id']
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
            node = root.find(f"{prefix}/{prefix}_{field}")
            if field == 'length':
                value = int(node.text)
            elif field == 'seqtype':
                value = node.get('value')
            else:
                value = node.text

            sequence_data[field] = value

        # save to database
        sequence_record = Sequence.objects.create(**sequence_data)

        # populate to singleton instance's variables
        cls._populate_variables({
            **sequence_data,
            id: sequence_record.id,
        })


    @classmethod
    def _load_from_db(cls) -> None:
        """
        Loads sequence data from database into memory
        """

        query_data = cls._get_query_data()

        # query data with the unique combination
        sequence_data = Sequence.objects.values('id','orgname', 'length', 'sequence').get(**query_data)

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
            print("Loading reference sequence from local DB")
            cls._load_from_db()
        except Sequence.DoesNotExist:
            print("Failed to load from DB. Querying NIH server")
            cls._remote_query()

        print(f"Loaded. \nSequence id:{cls.sequence_id} \nSequence name: {cls.name}, \nlength: {cls.sequence_length}")


    @classmethod
    def get(cls) -> (str, str):
        """
        Get sequence and its id

        :return: tuple of sequence string and id in db
        """

        if cls.sequence is None:
            raise Exception("No sequence available")

        return cls.sequence, cls.sequence_id













