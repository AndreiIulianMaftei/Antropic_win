# /Complete workflow/agents/research/openalex_agent.py
import requests
import time
import json
import asyncio
from typing import Dict, Any, Optional

# ==============================================================================
# Your provided synchronous data fetching logic (unchanged)
# ==============================================================================

def get_author_data_sync(name: str, affiliation: Optional[str] = None, top_n_publications: int = 10) -> str:
    """
    Fetches comprehensive author data from OpenAlex and returns it as a JSON string.
    NOTE: This is a synchronous and blocking function.
    """
    OPENALEX_BASE = "https://api.openalex.org"

    # --- Helper Functions ---
    def _search_author(name, affiliation):
        query = f'{OPENALEX_BASE}/authors?search={name}'
        try:
            resp = requests.get(query)
            resp.raise_for_status()
            results = resp.json().get('results', [])
            if not results: return None
            if affiliation:
                filtered = [
                    a for a in results if affiliation.lower() in
                    a.get('last_known_institution', {}).get('display_name', '').lower()
                ]
                return filtered[0] if filtered else results[0]
            return results[0]
        except requests.RequestException as e:
            print(f"API request error during author search: {e}")
            return None

    def _get_metrics(author_id):
        url = f"{OPENALEX_BASE}/authors/{author_id}"
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            a = resp.json()
            summary = a.get('summary_stats', {})
            return {
                'openalex_id': a.get('id'),
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
        except requests.RequestException:
            return {}

    def _get_publications(author_id, max_pubs):
        url = f"{OPENALEX_BASE}/works"
        params = {'filter': f'author.id:{author_id}', 'sort': 'cited_by_count:desc', 'per-page': min(max_pubs, 200)}
        try:
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            works = resp.json().get('results', [])
            return [{'id': w.get('id'), 'title': w.get('title'), 'cited_by_count': w.get('cited_by_count', 0)} for w in works][:max_pubs]
        except requests.RequestException:
            return []

    def _reconstruct_abstract(inverted_index):
        if not inverted_index: return None
        word_positions = [(pos, word) for word, positions in inverted_index.items() for pos in positions]
        word_positions.sort()
        return ' '.join([word for pos, word in word_positions])

    def _get_abstract(work_id):
        if not work_id: return "Abstract not available."
        url = f"{OPENALEX_BASE}/works/{work_id}"
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            work_data = resp.json()
            abstract = work_data.get('abstract')
            if not abstract and work_data.get('abstract_inverted_index'):
                abstract = _reconstruct_abstract(work_data.get('abstract_inverted_index'))
            return abstract or "Abstract not available."
        except requests.RequestException:
            return "Abstract not available."

    # --- Main Logic ---
    author = _search_author(name, affiliation)
    if not author:
        return json.dumps({"error": f"Author '{name}' not found."}, indent=4)

    author_id = author.get('id').split('/')[-1]
    metrics = _get_metrics(author_id)
    publications = _get_publications(author_id, max_pubs=top_n_publications)
    
    simplified_publications = []
    for pub in publications:
        work_id = pub['id'].split('/')[-1]
        abstract = _get_abstract(work_id)
        simplified_publications.append({'title': pub.get('title'), 'abstract': abstract, 'cited_by_count': pub.get('cited_by_count', 0)})
        time.sleep(0.1)

    final_data = {"author_metrics": metrics, "top_publications": simplified_publications}
    return json.dumps(final_data, indent=4)


# ==============================================================================
# Asynchronous wrapper to make the function orchestrator-friendly
# ==============================================================================

async def fetch_openalex_data(founder_name: str, university: str) -> Dict[str, Any]:
    """
    Asynchronously fetches OpenAlex data by running the synchronous
    get_author_data_sync function in a separate thread.
    """
    print(f"  -> [OpenAlex] Starting blocking fetch for: {founder_name}")
    try:
        # Run the blocking function in a separate thread and await the result
        author_json_string = await asyncio.to_thread(
            get_author_data_sync,
            name=founder_name,
            affiliation=university,
            top_n_publications=10
        )
        print(f"  -> [OpenAlex] Finished fetch for: {founder_name}")
        # Parse the JSON string into a Python dictionary before returning
        return json.loads(author_json_string)
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON response from OpenAlex data fetcher."}
    except Exception as e:
        return {"error": f"An unexpected error occurred during OpenAlex fetch: {e}"}