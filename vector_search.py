# -*- coding: utf-8 -*-

"""
Module for vector space search engine.

The technique uses algebra matrix to compare documents based on term frequency. A major concept is the term space which 
is unique words on a document. To calculate the frequency of each unique word, there is a second concept, the term counts
that record the count the frequency of the word in the document, create a concordance. 
With this concepts in mind we can create a dimensional vector, where each dimension is a unique word in the document.
"""

__description__ = 'Search the relation of a document using vector space theory'

import math
import re
from argparse import ArgumentParser, ArgumentTypeError

class VectorSearch(object):
    """
    The class to handle 
    """
    def __init__(self):
        """
        Initialize the vector search object. Create empty vector and the concordance list.
        """
        self.concordances = []
        self.magnitudes = []

    def add(self, concordance):
        """
        Index a new concordance to list calculating it's magnitude.

        :param concordance: The concordance class.
        """
        self.concordances.append(concordance)
        self.magnitudes.append(self.magnitude(concordance))

    def search_relation(self, document: str, ordered: bool=True):
        """
        Search the relation of the document with registered concordances.

        :param document: The document string to search.
        :return:<list> List with related concordances and respective cosigns.
        """
        result = []

        # Generate the concordance for the document.
        document_concordance = Concordance(document)
        
        # Calculate the documet magnitude value.
        document_magnitude = self.magnitude(document_concordance)
        for index, concordance in enumerate(self.concordances):
            # Iterate between all concordances querying the text concordance
            # with the actual concordance.
            #
            # Calculate the product of the document magnitude with the 
            # current concordance magnitude.
            denominator = document_magnitude * self.magnitudes[index]

            if denominator == 0:
                # Continue looping because denominator can not be zero.
                continue
            total = 0
            for count, word in concordance:
                if document_concordance.has(word):
                    # Sum the product of the concordance word frequency with 
                    # the document concordance.
                    total += count * document_concordance.get_frequency(word)
            # Calculate the cosign of the document.
            cosign = total / denominator
            if cosign != 0:
                result.append([cosign, concordance])
        if ordered:
            # Sort the result by high cosign value
            result = sorted(result, key=lambda item: item[0])
            result.reverse()
        return result

    def magnitude (self, concordance):
        """
        Calculate the maginute of a concordance class.
        :param concordance: The concordance class.
        :return: The magnitude value.
        """
        total = 0
        for count, word in concordance:
            total += count ** 2
        return math.sqrt(total)
        
class Concordance(object):
    """
    The concordance of a document.
    """
    def __init__(self, document: str):
        """
        Initialize a concordance object from a document string.
        :param document: The document.
        """
        self.original = document
        self.items = self._calculate_concordance(document)
        self.index = 0
        
    def get_frequency(self, word: str):
        """
        Returns the frequency of the word on the document, wheter on document.
        :param word: The word to find.
        :return:<int> The frequency value.
        """
        return self.items[word] if self.has(word) else 0

    def has(self, word: str):
        """
        Determine wheter a word is in document items.
        :param word: The word to find.
        :return:<bool> A boolean indicating wheter the word is in item.
        """
        return word in self.items

    def _calculate_concordance(self, document: str):
        """
        Calculate the frequency of each word on document.
        :param document: The string document.
        :return:<dict> A dictionary with the word and respective frequency.
        """
        # Filter the document words.
        plain_list = self._filter_words(document.split(' '))
        ocorrences = {}
        for word in plain_list:
            # Calculate each word ocorrence.
            if word in ocorrences:
                ocorrences[word] += 1
            else:
                ocorrences[word] = 1
        return ocorrences

    def _filter_words(self, plain: list):
        """
        Filter words from documents.
        :param plain: The string plain.
        :return:<list> The filtered document.
        """
        bad_words = self._get_bad_words()
        return [self._filter_word(word) for word in plain if word.lower() not in bad_words]

    def _get_bad_words(self):
        """
        List with words to be skipped. Generally are prepositions, pronouns...
        :return:<list> List with words.
        """
        return ['the', 'for', 'an', 'a', 'with', 'without']

    def _filter_word(self, word: str):
        """
        Remove special characteres from word to a more clean plain word.
        :param word: The word to filter.
        :return:<str> The filtered word.
        """
        chars = [',', '.', '(', ')', '[', ']']
        word = word.strip()
        for char in chars:
            # Replace each character in word.
            word = word.replace(char, '')
        return word

    def __iter__(self):
        """
        Implements iterator.
        :return:<object> The instance object.
        """
        self.index = -1
        return self

    def __next__(self):
        """
        Method to be called on iteration.
        :return:<list> The word frequency and the current word.
        """
        self.index += 1
        if self.index >= len(self.items):
            raise StopIteration
        # Get the current word in iteration.
        word = list(self.items.keys())[self.index]
        return self.items[word], word

def main():
    parser = ArgumentParser(usage='%(prog)s [options] document', description=__description__)
    parser.add_argument('-c', action='append', help='Read concordance file.', dest='concordances')
    parser.add_argument('-f', action='store', help='Read document search from file.', dest='document_file')
    parser.add_argument('--dont-sort', action='store_false', help='Do not sort the result.', dest='sort')
    parser.add_argument('--text-length', action='store', help='The length of the text to show. Default 100.', 
        type=int, default=100)
    parser.add_argument('document', action='append', nargs='*')
    # Get the parsed arguments from stdin.
    args = parser.parse_args()
    
    # Initialize the vector search with empty values.
    vector_search = VectorSearch()

    for file in args.concordances:
        with open(file) as file_buffer:
            # Read the concordance from file and index to vector.
            vector_search.add(Concordance(file_buffer.read()))

    if args.document_file:
        # Read the search from file.
        with open(args.document_file) as file_buffer:
            document = file_buffer.read()
    elif len(args.document[0]) > 0:
        # Create the document with the document list.
        document = ' '.join(args.document[0])
    else:
        raise ArgumentTypeError('A search document must be provided')

    print('[*] Searching for relations...')

    # Search the relation on concordances with the document file.
    result = vector_search.search_relation(document, args.sort)

    print('[+] Found {} relations!'.format(len(result)))
    for item in result:
        print('\nCosign: {}\nText: {}\n'.format(item[0], item[1].original[:args.text_length]))

if __name__ == '__main__':
    main()