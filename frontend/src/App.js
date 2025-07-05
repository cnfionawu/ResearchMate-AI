import React, { useState } from 'react';

function App() {
  const [query, setQuery] = useState('');
  const [papers, setPapers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError('');
    setPapers([]);

    try {
      const response = await fetch(`http://127.0.0.1:5000/search?query=${encodeURIComponent(query)}`);
      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.message || "Something went wrong");
      }
      const data = await response.json();
      setPapers(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '800px', margin: 'auto' }}>
      <h2>ResearchMate</h2>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter topic (e.g., GANs)"
        style={{ padding: '0.5rem', width: '70%' }}
      />
      <button onClick={handleSearch} style={{ marginLeft: '1rem' }}>
        Search
      </button>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {papers.length > 0 && (
        <div>
          <h3>Results:</h3>
          {papers.map((paper, i) => (
            <div key={i} style={{ marginBottom: '2rem' }}>
              <h4>{paper.title}</h4>
              <p><strong>Authors:</strong> {paper.authors}</p>
              <p>{paper.summary}</p>
              <p><em>Source: {paper.source}</em></p>
              <hr />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
