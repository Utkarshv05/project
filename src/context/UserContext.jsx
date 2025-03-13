import React, { createContext, useState } from "react"; 
import run from "../gemini";

export const DataContext = createContext();

function UserContext({ children }) {
  let [speaking, setSpeaking] = useState(false);
  let [prompt, setPrompt] = useState("Listening...");
  let [response, setResponse] = useState(false);
  const AI_NAME = "Cypher"; // AI's Name

  function speak(text) {
    let text_speak = new SpeechSynthesisUtterance(text);
    text_speak.volume = 1;
    text_speak.rate = 1;
    text_speak.pitch = 1;
    text_speak.lang = "en-US";
    window.speechSynthesis.speak(text_speak);
  }

  async function aiResponse(prompt) {
    let text = await run(prompt);
    let newText = text.replace(/google/gi, "Utkarsh Singh"); 
    setPrompt(newText);
    speak(newText);
    setResponse(true);
    setTimeout(() => {
      setSpeaking(false);
    }, 5000);
  }

  let speechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  let recognition;

  if (speechRecognition) {
    recognition = new speechRecognition();
    recognition.onresult = (e) => {
      let transcript = e.results[e.resultIndex][0].transcript;
      setPrompt(transcript);
      takeCommand(transcript.toLowerCase());
    };
  }

  function takeCommand(command) {
    let links = {
      youtube: "https://www.youtube.com/",
      google: "https://www.google.com/",
      gmail: "https://mail.google.com/",
      github: "https://github.com/Utkarshv05",
      linkedin: "https://www.linkedin.com/in/utkarsh-singh-lh999052004/",
    };

    // 📅 Get Current Date & Time
    let now = new Date();
    let time = now.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit", hour12: true });
    let date = now.toLocaleDateString("en-US", { weekday: "long", year: "numeric", month: "long", day: "numeric" });

    // 🎯 Recognizing AI's Name
    if (command.includes("hello") && command.includes(AI_NAME.toLowerCase())) {
      speak(`Hello! How can I assist you?`);
      setPrompt(`Hello! How can I assist you?`);
      return;
    }
    
    if (command.includes(AI_NAME.toLowerCase())) {
      speak(`Yes, I'm ${AI_NAME}. How can I help you?`);
      setPrompt(`Yes, I'm ${AI_NAME}. How can I help you?`);
      return;
    }

    // 🎯 Handle Website Commands
    for (let key in links) {
      if (command.includes("open") && command.includes(key)) {
        speak(`Opening ${key}`);
        setPrompt(`Opening ${key}...`);
        window.open(links[key], "_blank");
        setTimeout(() => {
          setSpeaking(false);
        }, 2000);
        return;
      }
    }

    // 🎯 Handle Date & Time
    if (command.includes("what") && command.includes("time")) {
      speak(`The current time is ${time}`);
      setPrompt(`The current time is ${time}`);
      return;
    }

    if (command.includes("what") && command.includes("date")) {
      speak(`Today's date is ${date}`);
      setPrompt(`Today's date is ${date}`);
      return;
    }

    aiResponse(command);
  }

  let value = {
    recognition,
    speak,
    speaking,
    setSpeaking,
    prompt,
    setPrompt,
    response,
    setResponse
  };

  return <DataContext.Provider value={value}>{children}</DataContext.Provider>;
}

export default UserContext;
