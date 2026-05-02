import React, { useState } from 'react';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const res = await fetch('/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Data Assistant</h1>
        <p>Ask questions about your sales and marketing data</p>
      </header>

      <main className="App-main">
        <form onSubmit={handleSubmit} className="query-form">
          <div className="input-group">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g., Top 2 products by revenue"
              className="query-input"
              disabled={loading}
            />
            <button type="submit" disabled={loading || !question.trim()} className="query-button">
              {loading ? 'Asking...' : 'Ask'}
            </button>
          </div>
        </form>

        {error && (
          <div className="error-message">
            <h3>Error:</h3>
            <p>{error}</p>
          </div>
        )}

        {response && (
          <div className="response-container">
            <div className="response-section">
              <h3>Your Question:</h3>
              <p>{response.question}</p>
            </div>

            <div className="response-section">
              <h3>Generated SQL:</h3>
              <pre className="sql-code">{response.sql_query}</pre>
            </div>

            <div className="response-section">
              <h3>Results:</h3>
              <div className="results-table">
                <table>
                  <thead>
                    <tr>
                      {response.column_names.map((col, idx) => (
                        <th key={idx}>{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {response.results.map((row, idx) => (
                      <tr key={idx}>
                        {row.map((cell, cellIdx) => (
                          <td key={cellIdx}>{String(cell)}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="response-section">
              <h3>Answer:</h3>
              <p>{response.answer}</p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;