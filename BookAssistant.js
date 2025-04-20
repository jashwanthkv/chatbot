import React, { useState } from 'react';
import axios from 'axios';

function ChatTerminal() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [userId, setUserId] = useState('');

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/perform-task', {
        task: input,
        user_id: userId.trim() || 'anonymous' // fallback for now
      });

      const botReply = response.data.result || '🤖 (No response)';
      setMessages(prev => [...prev, { sender: 'bot', text: botReply }]);

    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, { sender: 'bot', text: '⚠️ Error talking to agent.' }]);
    }
  };

  return (
    <div className="chat-terminal" style={{ maxWidth: 600, margin: 'auto', fontFamily: 'monospace' }}>
      <h2>📘 Book Assistant Terminal</h2>
      <input
        type="text"
        placeholder="User ID (email or any unique name)"
        value={userId}
        onChange={e => setUserId(e.target.value)}
        style={{ width: '100%', marginBottom: 8, padding: 8 }}
      />
      <div style={{ border: '1px solid #ccc', height: 400, overflowY: 'scroll', padding: 10 }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ textAlign: msg.sender === 'user' ? 'right' : 'left' }}>
            <pre><strong>{msg.sender === 'user' ? '🧑 You' : '🤖 Agent'}:</strong> {msg.text}</pre>
          </div>
        ))}
      </div>
      <input
        type="text"
        placeholder="Type here..."
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && handleSend()}
        style={{ width: '100%', padding: 8, marginTop: 8 }}
      />
      <button onClick={handleSend} style={{ width: '100%', padding: 10, marginTop: 4 }}>
        Send
      </button>
    </div>
  );
}

export default ChatTerminal;
