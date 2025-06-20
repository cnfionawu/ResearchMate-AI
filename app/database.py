import sqlite3
import arxiv
import os

DB_PATH = os.path.join("data", "papers.db")

# SQLite db initialize
def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS papers (
            id TEXT PRIMARY KEY,
            title TEXT,
            authors TEXT,
            summary TEXT,
            source TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Fetch papers from Arxiv API
def fetch_arxiv(query, max_results=20):
    print(f"Fetching from Arxiv: '{query}' ...")
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    results = []
    for result in search.results():
        paper_id = result.entry_id
        title = result.title.strip()
        authors = ", ".join([a.name for a in result.authors])
        summary = result.summary.strip()
        results.append((paper_id, title, authors, summary, "arxiv"))
    print(f"Found {len(results)} papers.")
    return results

# Save new papers to local DB
def save_papers(papers):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for paper in papers:
        try:
            c.execute(
                "INSERT OR IGNORE INTO papers (id, title, authors, summary, source) VALUES (?, ?, ?, ?, ?)",
                paper
            )
        except Exception as e:
            print(f"Error saving paper {paper[0]}: {e}")
    conn.commit()
    conn.close()

# Query papers from local DB (simple keyword match)
def query_papers_from_db(query):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT * FROM papers WHERE title LIKE ? OR summary LIKE ?",
        (f'%{query}%', f'%{query}%')
    )
    rows = c.fetchall()
    conn.close()
    return rows
