import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import time

def search_arxiv(query, max_results=10):
    url = f'http://export.arxiv.org/api/query?search_query={urllib.parse.quote(query)}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending'
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    root = ET.fromstring(data)
    
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    papers = []
    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
        id_url = entry.find('atom:id', ns).text
        arxiv_id = id_url.split('/abs/')[-1]
        pdf_url = id_url.replace('/abs/', '/pdf/') + '.pdf'
        papers.append({'title': title, 'id': arxiv_id, 'pdf_url': pdf_url})
    return papers

queries = ['all:"4D surface reconstruction"', 'all:"Dynamic surface reconstruction"', 'all:"4D Gaussian" AND all:"surface"']
all_papers = {}

for q in queries:
    print(f"Searching for: {q}")
    papers = search_arxiv(q, max_results=5)
    for p in papers:
        all_papers[p['id']] = p
    time.sleep(3) # be nice to arXiv API

print("=== RESULTS ===")
for p in all_papers.values():
    print(f"ID: {p['id']}")
    print(f"Title: {p['title']}")
    print(f"PDF: {p['pdf_url']}")
    print("---")
