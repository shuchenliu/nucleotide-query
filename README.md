# Nucleotide Query

## Introduction
This projects provides a web app for interactive regex matching against [SARS Cov Tor Nucleotide](https://www.ncbi.nlm.nih.gov/nuccore/30271926) as well as a CLI tool for matching [Homo sapiens chromosome 1, GRCh37.p13](https://www.ncbi.nlm.nih.gov/nuccore/NC_000001.10)

## Web app
#### 1. How to run  
You will need Docker cli tools including `docker-compose`.
> $DJANGO_ENV=production docker-compose up

This command will expose a web app at http://localhost.

#### 2. App Architecture  
The app uses `Django REST Framework` to build the API, with `Redis` as the caching backend. The app opt in the default use of `SQLite` with Django as the database.  Rather than using Django templates, the frontend was developed in `React` to enable rapid prototyping. An `NGINX` instance serves both the API and the built frontend application. All services and the building process are handled by `docker compose`. (`Google-re2`)[https://github.com/google/re2] is used at the app's core as a replacement for Python's `re` module for better efficiency.

#### 3. Model and View design  
- There are Four data models.  
> SearchTerm

This represents each valid *regex pattern* the API receives. 

> Match

Each matched location is persited into the database with `start` and `end` stored. It also establishes a `many-to-many` realtionship to `SearchTerm` as each a pattern could potentially returns many matches while the matched location could be produced by various patterns.

> Search

Each valid search is stored using the Search model. This serves two purposes: first, it decouples search terms and results, making data storage more structured and efficient, especially when there are duplicate searches; second, it enables analytical use cases such as retrieving the most frequent or recent searches.

> Sequence  

The target sequence is under 30kb, so loading it into memory from a local file poses no problem. However, since the frontend needs access to the sequence string to render match results, and to prepare for hypothetical future scaling with multiple sequences, it makes sense to store the sequence data independently.


- The API schema is highly correlated to the data models

  `GET /api/sequence/list` fetches a list of the metadata available nucleotide - in this case there's only one.  
  `GET /api/sequence/<sequence id>` fetches full length of a nucleotide sequence by its ID produced by `/sequence/list`  
  `GET /api/search/recent` fetches a list of recent conducted searches  
  `GET /api/search/frequent` fetches a list of searches conducted most frequently  
  `GET /api/query/?pattern=<pattern>` fetches a paginated results of the matched sequence locations for given regex pattern


## CLI tool
#### How to run
1. Use `docker-compose up` to start the containers
2. While running, open another terminal session and run `docker exec nucleotide-query-backend-1 python ./cli/cli-query.py <regrex term>`
This script will produced a unsored `mathc-{regrex term}` txt files as well as a cleaned-up version.

#### Under the hood
The script uses curl to download remote sequence data as needed, but defaults to loading from a local XML file if it exists. It chunks the sequence (`~250 MB`) into segments of `1,000,000` characters, with an overlapping region of `1,000` characters to reduce the chance of missing matches at the boundaries. The script then leverages multiprocessing to process these chunks in parallel. Matched locations are streamed back to the main process and written to a local file. Finally, it uses the sort CLI tool to deduplicate and sort the match positions in order.


## Challenges and Improvements

1. Dsitributed processing
Both the web app and CLI tool would benefit from incorporating Celery for asynchronous task delegation.
For example, the web app currently performs bulk creation of Match objects when a new SearchTerm is submitted, before returning paginated results to the frontend. While this is acceptable for smaller reference sequences, large-scale inserts and queries could overwhelm the database. Offloading this work to Celery would allow non-blocking processing, improving response times and scalability.
Similarly, the CLI tool aggregates matches from multiple processes and writes them line by line to a single file. With more time, I would refactor this to use Celery tasks that write to multiple smaller files in parallel, and concatenate them once all tasks complete. This would remove the bottleneck of a single-process write operation and make the tool more performant for very large sequences.

2. SQL Queries
One of the key challenges was generating a list of the most recent searches with distinct search terms. Due to limitations in SQLite and the complexity of writing efficient SQL for this use case, the solution I implemented remains suboptimal. With more time or a more robust database backend, I would explore subqueries more to better handle this logic.

3. Frontend Caveats
To prioritize rapid prototyping, many best practices in frontend development were set aside, particularly around state management and form handling. If given more time, I would adopt tools like XState for more structured state management and react-hook-form for more reliable form validation and control flow.

4. Fine tuning match logics
Even with parallel computing and/or dstibuted processing, the matching logic I implemented remains somewhat brute-force. I believe theare more efficient approaches of math techniques (like pre-indexing) with powerful text search tools like elasticsearch or specialized bioinformatics modules, which were left out of the scope of this project.









