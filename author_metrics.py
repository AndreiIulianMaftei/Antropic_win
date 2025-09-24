import requests

OPENALEX_BASE = "https://api.openalex.org"

def search_author_openalex(name, affiliation=None, top_n=5):
    """Search for authors by name (and filter by affiliation substring)."""
    query = f'{OPENALEX_BASE}/authors?search={name}'
    resp = requests.get(query)
    resp.raise_for_status()
    data = resp.json()
    results = data.get('results', [])
    if affiliation:
        # filter by affiliation name if present
        filtered = [a for a in results if affiliation.lower() in a.get('last_known_institution', {}).get('name', '').lower()]
        if filtered:
            return filtered
    return results[:top_n]

# def get_author_metrics_openalex(author_id):
#     """Given OpenAlex author id (e.g. “A12345…”), fetch metrics."""
#     url = f"{OPENALEX_BASE}/authors/{author_id}"
#     resp = requests.get(url)
#     resp.raise_for_status()
#     a = resp.json()
#     print(a)
#     # The API returns e.g. 'works_count', 'cited_by_count', etc.
#     metrics = {
#         'display_name': a.get('display_name'),
#         'works_count': a.get('works_count'),
#         'cited_by_count': a.get('cited_by_count'),
#         'h_index': a.get('h_index'),  # OpenAlex provides this
#         'i10_index': a.get('i10_index'),  # OpenAlex provides this
#         'last_known_institution': a.get('last_known_institution', {}).get('name'),
#         'orcid': a.get('orcid'),
#     }
#     return metrics
def get_author_metrics_openalex(author_id):
    """Given OpenAlex author id (e.g. “A12345…”), fetch metrics."""
    url = f"{OPENALEX_BASE}/authors/{author_id}"
    resp = requests.get(url)
    resp.raise_for_status()
    a = resp.json()

    summary = a.get('summary_stats', {})

    metrics = {
        'display_name': a.get('display_name'),
        'works_count': a.get('works_count'),
        'cited_by_count': a.get('cited_by_count'),
        'h_index': summary.get('h_index'),
        'i10_index': summary.get('i10_index'),
        'last_known_institution': (
            a.get('last_known_institutions', [{}])[0].get('display_name')
            if a.get('last_known_institutions') else None
        ),
        'orcid': a.get('orcid'),
    }
    return metrics

if __name__ == "__main__":
    name = "Yann Le Cun"
    affiliation = ""
    authors = search_author_openalex(name, affiliation)
    if not authors:
        print("No authors found in OpenAlex.")
    else:
        # pick first match
        author = authors[0]
        print("Candidate:", author.get('display_name'), author.get('id'))
        metrics = get_author_metrics_openalex(author['id'])
        print(metrics)
