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

* ```-c```:
Concordances are the frequency where a word repeats on a given text. Here you set the file text to read a text indexing the text on the search.

* ```-f```
The search text to read from a file. 

* ```--dont-sort```:
Do not sort the result by the result cosign.

* ```--text-length```:
Text length displayed on result.

* ```document```: 
Postional argument that is the raw text to search. You can use this option or write the text to a file and use the ```-f``` option.

### Result

```shell
$ python3 vector_search.py -c text1.txt -c text4.txt -c text3.txt sex
[*] Searching for relations...
[+] Found 2 relations!

Cosign: 0.5
Text: vaginas, penis, pussy, sex


Cosign: 0.02540822292337563
Text: Perhaps far exposed age effects. Now distrusts you her delivered applauded affection out sincerity.

```
