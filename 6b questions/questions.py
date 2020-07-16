import nltk
import sys
import os
import string
import math
from collections import Counter

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    file_names = os.listdir(directory)

    file_paths = map(
        lambda file_name: os.path.join(directory, file_name),
        file_names
    )

    mapping = dict()

    for filename, filepath in zip(file_names, file_paths):
        with open(filepath, encoding="utf8") as f:
            # print(filepath)
            mapping[filename] = f.read()

    return mapping


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    document = document.translate(str.maketrans('', '', string.punctuation))
    document = document.lower()

    stopwords = nltk.corpus.stopwords.words("english")

    return list(filter(
        lambda x: x not in stopwords,
        nltk.word_tokenize(document)
    ))


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    def idf(n):
        return math.log(len(documents)/n)

    # convert word list to set
    documents = documents.copy()
    for key, val in documents.items():
        documents[key] = set(val)

    counter = Counter()

    for word_set in documents.values():
        counter.update(word_set)

    idfs = dict()

    for word, count in counter.items():
        idfs[word] = idf(count)

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfs = dict(zip(
        files,
        map(Counter, files.values())
    ))

    def score(file):
        return sum(map(
            lambda word: tfs[file][word] * idfs[word],
            query
        ))
    
    # # debug
    # def score2(file):
    #     for word in query:
    #         print("^", word, tfs[file][word])
    #     return sum(map(
    #         lambda word: tfs[file][word] * idfs[word],
    #         query
    #     ))
    # 
    # print()
    # for file in files:
    #     print(file, score2(file))
    # print()

    return list(sorted(files, key=score, reverse=True))[:n]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    def query_term_density(sentence):
        return sum(map(
            lambda word: 1 if word in query else 0,
            sentences[sentence]
        )) / len(sentences[sentence])
    
    def score(sentence):
        matching_words = query & set(sentences[sentence])
        return sum(map(
            lambda word: idfs[word],
            matching_words
        ))

    return list(sorted(
        sentences,
        key = lambda s: (score(s), query_term_density(s)),
        reverse=True
    ))[:n]

    # # debug
    # output = list(sorted(
    #     sentences,
    #     key = lambda s: (score(s), query_term_density(s)),
    #     reverse=True
    # ))[:3]

    # return [s + " *" + str(score(s)) + " **" + str(query_term_density(s)) + " ***" + str(query) + "\n"
    # + "****" + str(sentences[s]) + "\n"
    
    #     for s in output
    # ]
        


if __name__ == "__main__":
    main()
