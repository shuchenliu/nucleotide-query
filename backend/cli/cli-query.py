import sys
import subprocess
import xml.etree.ElementTree as ET
from multiprocessing import Pool, cpu_count
from typing import List, Tuple
import re2 as re
from django.urls.resolvers import RegexPattern

URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
PARAMS = {
    "db": "nucleotide",
    "id": "224589800",
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


# XML methods copied from api part
def parse_xml(xml: bytes) -> str:
    prefix = "TSeq"
    root = ET.fromstring(xml)
    name = root.find(f"{prefix}/{prefix}_orgname").text
    sequence_length = int(root.find(f"{prefix}/{prefix}_length").text)
    sequence = root.find(f"{prefix}/{prefix}_sequence").text
    return sequence


def remote_query():
    # use curl for better progress displaying
    subprocess.run(["./get_file.sh"], check=True)


def load_xml():
    with open('224589800.xml', "rb") as f:
        contents = f.read()
        return parse_xml(contents)

def check_file():
    try:
        open('224589800.xml', "rb")
        return True
    except FileNotFoundError:
        return False


def chunk_with_overlap(total_length:int, size: int, overlap: int) -> List[Tuple[int, int]]:
    """
    Chunks sequence in defined sizes

    :param total_length: total length of sequence
    :param size: size of each chunk
    :param overlap: size of the chunk overlaps - this effectively decides the longest matched length
    :return: a tuple of (start, end) position denoting each chunk
    """
    chunks = []
    for i in range(0, total_length, size - overlap):
        start = i
        end = min(i + size, total_length)
        chunks.append((start, end))
    return chunks

def regex_each_chunk(args) -> List[Tuple[int, int]]:
    """
    Starts the regrex matching process on each chunk

    :param args:
        sequence: sequence string
        start, end: position denoting each chunk
         regex_comp: precompiled regex pattern, since we are querying one pattern each time
    :return:  (start, end) denoting each matched sequence
    """
    sequence, start, end, regex_comp = args
    matches = []
    chunk = sequence[start:end]
    for match in regex_comp.finditer(chunk):
        matches.append((
            start + match.start(),
            start + match.end(),
        ))
    return matches


def parallel_regex(sequence: str, regex_comp: RegexPattern, chunk_size: int = 10 ** 6, overlap: int = 10 ** 3):
    """
    Run regex task on each chunk in a parallel fashion

    :param sequence:  sq
    :param regex_comp: compiled regex pattern
    :param chunk_size: size of each chunk
    :param overlap: length of chunk overlaps
    :return: yields matches
    """
    chunks = chunk_with_overlap(len(sequence), chunk_size, overlap)

    args = [(sequence, start, end, regex_comp) for start, end in chunks]

    # multi-processing
    with Pool(cpu_count()) as pool:
        # use imap to yield match; order can be handled later
        for group in pool.imap_unordered(regex_each_chunk, args):
            for match in group:
                yield match



def main():

    # parse input regex from argument
    if len(sys.argv) > 1:
        regex_pattern = sys.argv[1]
        print(f"regex pattern passed in: {regex_pattern}")
    else:
        raise Exception('A regex mush be provided.')

    # precompile regex
    try:
        regex_comp = re.compile(regex_pattern)
    except re.error:
        raise Exception('Invalid regex pattern')


    # check if xml file already exists locally
    if not check_file():
        print("Local file not found. Downloading...")
        remote_query()
        print("Download complete.")

    # load xml into memory from disk
    sequence = load_xml()

    assert sequence is not None

    count = 0
    filename = f'matches-{regex_pattern}.txt'

    # write to file in the main process
    with open(filename, "w") as f:
        for start, end in parallel_regex(sequence, regex_comp):
            # write to line
            f.write(f"{start},{end}\n")

            count += 1
            if count % (10 ** 4) == 0:
                print(f"... found {count} matches so far", end="\r")

    print(f"Wrote {count} matches to {filename}")
    print ("Use bash to sort and remove duplicates")

    subprocess.run(["./clean_up.sh", filename], check=True)




if __name__ == "__main__":
    main()