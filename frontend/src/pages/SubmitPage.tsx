import React, { useState } from 'react';
import axios from 'axios';

const SubmitPage = () => {
  const [username, setUsername] = useState('');
  const [code, setCode] = useState('');
  const [response, setResponse] = useState<any>(null);

  const handleSubmit = async () => {
    try {
      const res = await axios.post('http://localhost:8000/submit', {
        username,
        code
      });
      setResponse(res.data);
    } catch (err: any) {
      setResponse({ error: err.message });
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Submit Your Code</h2>
      <input
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        style={{ display: 'block', marginBottom: '1rem', width: '300px' }}
      />
      <textarea
        placeholder="Paste your code here"
        value={code}
        onChange={(e) => setCode(e.target.value)}
        style={{ width: '600px', height: '300px' }}
      />
      <br />
      <button onClick={handleSubmit} style={{ marginTop: '1rem' }}>Submit</button>

      {response && (
        <pre style={{ marginTop: '2rem', background: '#f5f5f5', padding: '1rem' }}>
          {JSON.stringify(response, null, 2)}
        </pre>
      )}
    </div>
  );
};

export default SubmitPage;
