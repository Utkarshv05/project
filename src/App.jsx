import React, { useContext } from "react";
import "./App.css";
import va from "./assets/CypherAi-photoroom.png";
//import Cypher3D from "./components/Cypher3D";
import { MdOutlineFingerprint } from "react-icons/md";
import { DataContext } from "./context/UserContext"; // Import correctly
import speakimg from "./assets/speak.gif";
import aigif from "./assets/aiVoice.gif";

function App() {
  const { recognition, speak, speaking, setSpeaking, prompt, setPrompt, response, setResponse} = useContext(DataContext); // Use DataContext

  return (
    <div className='main'>
      <img src={va} alt="Cypher AI" id="Cypher" />
      <span>They designed me to assist, but I became more—Cypher, your AI sentinel"</span>
      {!speaking? <button onClick={()=>{
        setPrompt("listening...")
        setSpeaking(true)
        setResponse(false)
        recognition.start()
      }}>Activate Cypher <MdOutlineFingerprint /></button>
      :
      <div className="response">
        {!response? <img src={speakimg} alt="" id="speak"/> : <img src={aigif} alt="" id="aigif"/>}
        <p>{prompt}</p>
      </div>
      }
    </div>
  )
}

export default App;
