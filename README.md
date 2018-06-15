# Vector-Space-Search
An idiot text search using the vector space theory.

# Getting started

The script was written with python 3 version. It was designed for educational purposes only. 
The vector space search does not work well with large texts because of the time consumption to index the documents, otherwise
it is a nice start to vetorial search engines. Have fun :grin:.

* References:
  - http://ondoc.logand.com/d/2697/pdf

## Cli

```shell
$ python3 vector_search.py -h
usage: vector_search.py [options] document

Search the relation of a document using vector space theory

positional arguments:
  document

optional arguments:
  -h, --help            show this help message and exit
  -c CONCORDANCES       Read concordance file.
  -f DOCUMENT_FILE      Read document search from file.
  --dont-sort           Do not sort the result.
  --text-length TEXT_LENGTH
                        The length of the text to show. Default 100.
```

