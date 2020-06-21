import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    numlinks = len(corpus[page])

    # • If page has no outgoing links, then transition_model should return a probability distribution that chooses randomly among all pages with equal probability. (In other words, if a page has no links, we can pretend it has links to all pages in the corpus, including itself.)
    if numlinks == 0:
        p = 1 / len(corpus)
        return {page_: p for page_ in corpus}

    # • With probability damping_factor, the random surfer should randomly choose one of the links from page with equal probability.
    p1 = 1 / numlinks * damping_factor
    model1 = {page_: p1 for page_ in corpus[page]}

    # • With probability 1 - damping_factor, the random surfer should randomly choose one of all pages in the corpus with equal probability.
    p2 = 1 / len(corpus) * (1 - damping_factor)
    model2 = {page_: p2 for page_ in corpus}

    model = {page_: model1.get(page_, 0) + model2[page] for page_ in corpus}
    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    counts = {page: 0 for page in corpus}  # to record page counts

    current = random.choices(list(corpus))[0]  # current page
    # print("current", current)
    counts[current] += 1

    for _ in range(n - 1):
        model = transition_model(corpus, current, DAMPING)
        # move to next page
        current = random.choices(list(model), list(model.values()))[0]
        # keep count
        counts[current] += 1

    assert sum(counts.values()) == n, "(sum of counts) != n"

    return {page: count/n for page, count in counts.items()}


def iterate_pagerank(corpus0, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    corpus_size = len(corpus0)

    all_pages = set(corpus0)
    # • A page that has no links at all should be interpreted as having one link for every page in the corpus (including itself).
    corpus = {page: links if len(links) > 0 else all_pages
              for page, links in corpus0.items()
              }

    pages_that_link_to_me = {
        me: [page for page, links in corpus.items() if me in links]
        for me in corpus
    }
    numlinks = {page: len(links) for page, links in corpus.items()}

    pageranks = {page: 1/corpus_size for page in corpus}

    # iterative algorithm
    d = damping_factor
    first_term = (1-d)/corpus_size
    pr = pageranks
    count_consecutive_updates_within_threshold = 0
    while count_consecutive_updates_within_threshold < corpus_size:
        for p in corpus:
            new_pagerank = (
                first_term +
                d * sum(pr[i]/numlinks[i]
                        for i in pages_that_link_to_me[p]
                        )
            )
            if abs(pageranks[p] - new_pagerank) < 0.0001:
                # increment whenever an update is within threshold
                count_consecutive_updates_within_threshold += 1
            else:
                # reset whenever an update exceeds threshold
                count_consecutive_updates_within_threshold = 0
            # update pagerank
            pageranks[p] = new_pagerank

    return pageranks


if __name__ == "__main__":
    main()
