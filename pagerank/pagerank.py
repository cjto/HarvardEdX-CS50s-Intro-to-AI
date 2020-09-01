import os
import random
import re
import sys
import math

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
    distribution = {}
    links = len(corpus[page])

    if links != None:            
        for link in corpus:
            distribution[link] = (1 - damping_factor) / len(corpus)

        for link in corpus[page]:
            distribution[link] += damping_factor / links
    else:
        for link in corpus:
            distribution[link] = 1 / len(corpus)
    
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.
    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pageRankDict = {}
    for page in corpus.keys():
        pageRankDict[page] = 0

    for sample in range(n):
        if sample == None:
            # Picks ranom page
            page = random.choice(list(corpus.keys()))

        # Next model is previous based on transition model
        model = transition_model(corpus, page, damping_factor)
        for key in model.keys():
            pageRankDict[key] = pageRankDict[key] + model[key]

        population = list(model.keys())
        weights = list(model.values())
        page = random.choices(population, weights=weights)[0]

    # Normalize
    for page in corpus:
        pageRankDict[page] /= n

    return pageRankDict     


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.
    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pageRank = {}
    newRank = {}

    for page in corpus:
        pageRank[page] = 1 / len(corpus)

    loop = True

    #Generates new rank values
    while loop == True:
        for page in pageRank:
            total = 0

            for possible in corpus:
                # Iterates through the possible pages that can link to the current page
                if page in corpus[possible]:
                    total += pageRank[possible] / len(corpus[possible])
                if not corpus[possible]:
                    # Page no links == one link every page
                    total += pageRank[possible] / len(corpus)

            newRank[page] = (1 - damping_factor) / len(corpus) + damping_factor * total

        loop = False

        # If any of the values changes > threshold, repeat loop
        for page in pageRank:
            if not math.isclose(newRank[page], pageRank[page], abs_tol=0.001):
                loop = True
            pageRank[page] = newRank[page]

    return pageRank


if __name__ == "__main__":
    main()
