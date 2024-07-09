import React from 'react';
import logo from './logo.png';
import placeholderImage from './bg.jpg'; 

const ChatWindow = ({ messages }) => {
    return (
        <div className="container">
            <div className="header">
                <div className="logo-container">
                    <img src={logo} alt="Health Logo" className="logo" />
                </div>
                <h1 className="title">Dr Chat</h1>
            </div>
            <div className="main-content">
                <div className="left-section">
                    <div className="description">
                        <h2>Welcome to Dr Chat</h2>
                        <p>Interact with your HealthCare Assistant and boil-down your problems with the best solutions</p>
                    </div>
                    <img src={placeholderImage} alt="DescriptionImage" className="description-image" />
                </div>
                <div className="right-section">
                    <div className="chat-window">
                        {messages.map((msg, index) => (
                            <div key={index} className={`chat-message ${msg.sender}`}>
                                <strong>{msg.sender}: </strong>
                                <pre>{msg.text}</pre>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChatWindow;
