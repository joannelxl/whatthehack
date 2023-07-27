import React, { useState } from "react";
import "./HomePage.css";
import "../App.css";

function HomePage() {
  const [messages, setMessages = useState([
    message: "Hello, I am ChatGPT!"
    sender: "ChatGPT"
  ]) //[]
  return (
    <>
      <div className="homepage-content">

      </div>

    </>
  );
}

export default HomePage;
