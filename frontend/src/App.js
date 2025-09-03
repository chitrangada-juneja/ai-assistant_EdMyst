import React, { useState } from 'react';
import './App.css';
import { askFromBackend } from './api';
import { ReactComponent as ChatIcon } from './chat-bubble.svg';
import { ReactComponent as Ellipse } from './blue-ellipse.svg';
import Hover from './components/Hover';
import {ReactComponent as EdyAvatar} from './components/Edy.svg';
import {ReactComponent as SendButton} from './send-button.svg';
import { ReactComponent as PaperclipIcon } from './paperclip.svg';
import { useEffect, useRef } from "react";

import ReactMarkdown from "react-markdown";
function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    {
      role: 'bot',
      text: "Hi! I'm Edy! How can I assist you with EdMyst queries today ?",
      link: ''
    }
  ]);
  const [isChatOpen, setIsChatOpen] = useState(false);      //to check if the chat is open  
  const [showPreview, setShowPreview] = useState(false);
  const[hasMessage, setHasMessage] = useState(false); 
  
  const [selectedFile, setSelectedFile] = useState(null);
const toggleChat = () => {
  setIsChatOpen(prev => !prev);
};

const sendMessage = async () => {
  if (!input.trim() && !selectedFile) return;

  const userMsg = input.trim();
  setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
  setInput('');

  const formData = new FormData();
  formData.append("message", userMsg || ""); // always send message, even if empty
  if (selectedFile) {
    formData.append("file", selectedFile);
  }

  try {
    const response = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Upload failed");
    }

    const data = await response.json();

    // send userMsg to your existing askFromBackend
    const botReply = await askFromBackend(userMsg);

    setMessages(prev => [
      ...prev,
      {
        role: 'bot',
        text: botReply.answer,
        link: botReply.link || '',
      },
    ]);

    // reset file after send
    setSelectedFile(null);

  } catch (error) {
    console.error("Error:", error);
    setMessages(prev => [
      ...prev,
      {
        role: 'bot',
        text: "An error occurred while processing your request.",
        link: '',
      },
    ]);
  }
};




  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
      setHasMessage(true)
    }
  };

  
  const chatRef = useRef(null);

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]); // run when messages change




  return (
    <div className="App">
     

     {isChatOpen && (
  <div className="chat-container">
    
    {/* Header with logo + text */}
    <div className="chat-header">
      <div className="logo-text-container">
        <div className="logo-circle">
          <EdyAvatar className="edy-avatar" />
        </div>
        <span className="header-text">✨ Edy from EdMyst ✨</span>
      </div>
    </div>

    {!hasMessage && (
      <div className="chat-subtitle">
        Responses are generated using AI and may contain mistakes.
      </div>
    )}

    <div className="chat-box" ref = {chatRef}>
      {messages.map((msg, index) => (
        <div
          key={index}
          className={`message ${msg.role === 'user' ? 'user-message' : 'bot-message'}`}
        >
          <div className="markdown">

         <ReactMarkdown
  components={{
    a: ({ node, ...props }) => (
      <a
        {...props}
        style={{
          fontSize: "16px",  // control size
          display: "inline", // prevent new line
          textDecoration: "underline",
          color: "blue"
        }}
      />
    ),
    // stops <p> from wrapping
  }}
>
          {msg.text}</ReactMarkdown>
         </div>
          </div>
          ))}
        </div>
    
    

          <div className="input-box">
          <div className="input-wrapper">
        
            <input
              type="text"
              placeholder="Ask a question..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
            />
            <label className = "file-upload-label">
              
              <PaperclipIcon className= "paperclip-icon" />
              
              <input 
              type= "file"
              accept = ".pdf"
              onChange= {(e) =>  setSelectedFile(e.target.files[0])}
              style= {{display : 'none'}}
              />
            </label>
            </div>
            <button className="input-box-button" onClick={sendMessage}>
              <SendButton />
            </button>
          </div>
        </div>
      )}
       <div
      className="chat-hover-wrapper"
      onMouseEnter={() => setShowPreview(true)}
      onMouseLeave={() => setShowPreview(false)}
    >
     
      {showPreview && !isChatOpen && <Hover onClose={() => setShowPreview(false)} />}

      <div className="chat-toggle" onClick={toggleChat}>
         <div className="chat-button-layer">
        <Ellipse className="chat-ellipse" />
        <ChatIcon className="chat-icon" />
        </div>
      </div>

    </div>
      
    </div>
  );
};

export default App;



//<div className= "paperclip-button">