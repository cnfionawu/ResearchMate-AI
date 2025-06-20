import sqlite3
import arxiv
import os
import time

DB_PATH = os.path.join("data", "papers.db")

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
    c.execute('''
        CREATE TABLE IF NOT EXISTS query_cache (
            query TEXT PRIMARY KEY,
            last_fetched INTEGER
        )
    ''')
    conn.commit()
    conn.close()


def fetch_arxiv(query, max_results=20):
    print(f"Fetching from Arxiv: '{query}' ...")
    start_time = time.time()

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

    end_time = time.time()
    print(f"Found {len(results)} papers in {end_time - start_time:.2f} seconds.")
    return results


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


def get_all_papers_from_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM papers")
    rows = c.fetchall()
    conn.close()
    return rows


def get_query_last_fetched(query):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT last_fetched FROM query_cache WHERE query = ?", (query,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None


def update_query_timestamp(query):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT OR REPLACE INTO query_cache (query, last_fetched) VALUES (?, ?)",
        (query, int(time.time()))
    )
    conn.commit()
    conn.close()
