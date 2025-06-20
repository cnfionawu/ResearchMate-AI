from flask import Flask, request, jsonify
from app.database import init_db, fetch_arxiv, save_papers, query_papers_from_db
from app.retrieval import hybrid_search
from app.summarizer import summarize

app = Flask(__name__)
init_db()

@app.route('/search')
def search():
    # Check and get query param
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Query parameter required"}), 400

    # Always fetch from Arxiv
    new_papers = fetch_arxiv(query)
    save_papers(new_papers)

    # Optional: merge with cached ones
    local_results = query_papers_from_db(query)
    print(f"Local results found: {len(local_results)}")
    if not local_results:
        return jsonify({"message": f"No papers found for query '{query}'."}), 404

    # Hybrid retrieval
    ranked = hybrid_search(query, local_results)

    # Summarize top N
    top = ranked[:5]
    summaries = summarize([paper[3] for paper in top])  # abstract is at index 3

    # Return papers with info
    return jsonify([
        {
            "title": paper[1],
            "authors": paper[2],
            "summary": s,
            "source": paper[4]
        } for paper, s in zip(top, summaries)
    ])
