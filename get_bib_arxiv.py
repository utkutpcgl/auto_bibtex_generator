import arxiv
import time
from difflib import SequenceMatcher

SIMILARITY_THRESHOLD = 0.9

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def get_best_match(results, title):
    # results = list(i for i in results)
    best_match = None
    highest_similarity = 0
    try:
        for candidate_id, result in enumerate(results):
            result_title = result.title.strip()
            similarity = similar(title.lower(), result_title.lower())
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = result
                if highest_similarity > SIMILARITY_THRESHOLD:
                    break
    except arxiv.UnexpectedEmptyPageError:
        return best_match, highest_similarity
    return best_match, highest_similarity

def search_and_get_best_match(query,client,title):
    search = arxiv.Search(
        query=query,
        max_results=10000,
        sort_by=arxiv.SortCriterion.Relevance
    )
    results = client.results(search)
    best_match, highest_similarity = get_best_match(results, title)
    return best_match, highest_similarity

def try_until_best_match_found(client,author, title):
    query = f'ti:{title} AND au:{author}' #  AND au:{author}
    query_titleonly = f'ti:{title}' #  AND au:{author}
    query_authoronly = f'au:{author}'
    best_match, highest_similarity = search_and_get_best_match(query=query,client=client,title=title)
    if not best_match:
        best_match, highest_similarity = search_and_get_best_match(query=query_titleonly,client=client,title=title)
    if not best_match:
        best_match, highest_similarity = search_and_get_best_match(query=query_authoronly,client=client,title=title)
    return best_match, highest_similarity
    

def get_arxiv_bibtex(author, title:str, citation_key):
    # Construct the default API client.
    client = arxiv.Client()
    best_match, highest_similarity = try_until_best_match_found(client=client, author=author, title=title)

    if best_match and highest_similarity > 0.8:  # adjust the threshold as needed
        arxiv_id = best_match.entry_id.split('/')[-1]
        arxiv_id_no_version = arxiv_id.split('v')[0]
        authors = ' and '.join([f"{name.split()[-1]}, {' '.join(name.split()[:-1])}" for name in [a.name for a in best_match.authors]])
        bibtex = f"@article{{ {citation_key},\n"
        bibtex += f"  title={{ {best_match.title} }},\n"
        bibtex += f"  author={{ {authors} }},\n"
        bibtex += f"  journal={{ arXiv preprint arXiv:{arxiv_id_no_version} }},\n"
        bibtex += f"  year={{ {best_match.published.year} }},\n"
        if best_match.doi:
            bibtex += f"  doi={{ {best_match.doi} }},\n"
        bibtex += f"  eprint={{ {arxiv_id_no_version} }},\n"
        bibtex += f"  eprinttype={{ arXiv }},\n"
        bibtex += f"  url={{ {best_match.entry_id} }}\n"
        bibtex += "}"
        return bibtex
    return None

def process_papers(papers):
    bibtex_entries = []
    for author, title, citationkey in papers:
        bibtex = get_arxiv_bibtex(author, title, citationkey)
        if bibtex:
            bibtex_entries.append(bibtex)
            print(f"{bibtex}")
        else:
            print(f"#No BibTeX found for the paper '{title}' by '{author}' with citation key: '{citationkey}'")
        time.sleep(15)  # Corrected rate limiting to comply with arXiv's terms of use
    return bibtex_entries

def fix_paper_titles(raw_papers):
    """Remove ":" from the titles, breaks arxiv search."""
    fixed_papers = []
    for paper in raw_papers:
        fixed_paper = (paper[0], paper[1].replace(":",""), paper[2])
        fixed_papers.append(fixed_paper)
    return fixed_papers

# Example usage
raw_papers = [
    ("Srinivas", "Simulated Annealing Algorithm for Deep Learning", "srinivas2010simulated"),
    ("Zhang", "A Closer Look at Memorization in Deep Networks", "zhang2017closer"),
    ("Senior", "Learning-Rate Annealing Methods for Deep Neural Networks", "senior2013learning"),
    ("Baydin", "No More Pesky Learning Rates", "baydin2017nomore"),
    ("Smith", "Super-Convergence: Very Fast Training of Neural Networks Using Large Learning Rates", "smith2017super"),
    ("Smith", "Cyclical Learning Rates for Training Neural Networks", "smith2017cyclical"),
    ("Loshchilov", "SGDR: Stochastic Gradient Descent with Warm Restarts", "loshchilov2016sgdr"),
    ("Kingma", "Adam: A Method for Stochastic Optimization", "kingma2014adam"),
]


fixed_papers = fix_paper_titles(raw_papers=raw_papers)
# Example usage with your defined list of papers
bibtex_entries = process_papers(fixed_papers)
