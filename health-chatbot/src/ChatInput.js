import React, { useState } from 'react';

const ChatInput = ({ addMessage, clearMessages }) => {
  const [input, setInput] = useState('');
  const [awaitingDays, setAwaitingDays] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (input.trim()) {
      addMessage({ sender: 'You', text: input });

      if (awaitingDays) {
        setAwaitingDays(false);
        await sendToBackend(input, true);  
      } else {
        await sendToBackend(input);
      }

      setInput('');
    }
  };

  const handleReloadChat = () => {
    clearMessages(); 
    setInput('');
  };

  const sendToBackend = async (input, isDays = false) => {
    try {
      const userId = 'unique_user_id';  

      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input, user_id: userId })
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      addMessage({ sender: 'Bot', text: data.message });

      if (data.message.includes('Please enter the total number of days')) {
        setAwaitingDays(true);
      }

    } catch (error) {
      console.error('Error fetching prediction:', error);
      addMessage({ sender: 'Bot', text: 'There was an error fetching the prediction. Please try again later.' });
    }
  };

  return (
    <form className="chat-input" onSubmit={handleSubmit}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Enter your input..."
      />
      <button type="submit">Send</button>
      <button type="button" onClick={handleReloadChat}>Reload Chat</button>
    </form>
  );
};

export default ChatInput;
