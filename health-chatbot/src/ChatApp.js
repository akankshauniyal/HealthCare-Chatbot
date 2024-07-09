import React, { useState } from 'react';
import ChatWindow from './ChatWindow';
import ChatInput from './ChatInput';
import './ChatApp.css';

const initialMessage = {
  sender: 'Bot',
  text: 'Hi! We are happy to see you here, type "bye" in case you would like to end the conversation'
};

const ChatApp = () => {
  const [messages, setMessages] = useState([initialMessage]);

  const clearMessages = () => {
    setMessages([initialMessage]); 
  };
  
  const addMessage = (message) => {
    setMessages((prevMessages) => [...prevMessages, message]);
  };

  return (
    <div className="chat-app">
      <ChatWindow messages={messages} />
      <ChatInput addMessage={addMessage} clearMessages={clearMessages} />
      
    </div>
    
  );
};

export default ChatApp;
