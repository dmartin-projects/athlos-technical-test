import logo from './logo.svg';
import './App.css';
import { useState } from 'react';

function App() {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const testBackendConnection = async () => {
    setLoading(true);
    try {
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const res = await fetch(`${apiUrl}/api/v1/scrapper/test/`);
      const data = await res.json();
      setResponse(data);
    } catch (error) {
      setResponse({ error: error.message });
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <button onClick={testBackendConnection} disabled={loading}>
          {loading ? 'Testing...' : 'Test Backend Connection'}
        </button>
        {response && (
          <div style={{ marginTop: '20px', padding: '10px', background: '#282c34', borderRadius: '5px' }}>
            <pre>{JSON.stringify(response, null, 2)}</pre>
          </div>
        )}
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
