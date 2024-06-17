import arxiv
import time
from difflib import SequenceMatcher

SIMILARITY_THRESHOLD = 0.9

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def get_arxiv_bibtex(author, title:str, citation_key):
    # Construct the default API client.
    client = arxiv.Client()
    query = f'ti:{title} AND au:{author}' #  AND au:{author}
    search = arxiv.Search(
        query=query,
        max_results=10000,
        sort_by=arxiv.SortCriterion.Relevance
    )
    results = client.results(search)
    # results = list(i for i in results)
    best_match = None
    highest_similarity = 0

    for candidate_id, result in enumerate(results):
        result_title = result.title.strip()
        similarity = similar(title.lower(), result_title.lower())
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = result
            if highest_similarity > SIMILARITY_THRESHOLD:
                break

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
        bibtex += "}\n"
        return bibtex
    return None

def process_papers(papers):
    bibtex_entries = []
    for author, title, citationkey in papers:
        bibtex = get_arxiv_bibtex(author, title, citationkey)
        if bibtex:
            bibtex_entries.append(bibtex)
            print(f"\n{bibtex}")
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
    ("Howard", "MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications", "howard2017mobilenets"),
    ("Tan and Le", "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks", "tan2019efficientnet"),
    ("He", "Deep Residual Learning for Image Recognition", "he2016deep"),
    ("Huang", "Densely Connected Convolutional Networks", "huang2017densely"),
    ("Wang", "Deep High-Resolution Representation Learning for Visual Recognition", "wang2019deep"),
    ("Dai", "Deformable Convolutional Networks", "dai2017deformable")
]

fixed_papers = fix_paper_titles(raw_papers=raw_papers)
# Example usage with your defined list of papers
bibtex_entries = process_papers(fixed_papers)
