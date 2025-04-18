import React from "react";
import { Routes, Route } from "react-router-dom";
import Home from "./Home";
import ProductScan from "./ProductScan";
import Homepage from "./Homepage";
import ExportData from "./Dataextract";
function App() {
  return (
    <Routes>
      <Route path="/" element={<Homepage />} />
      <Route path="/home" element={<Home />} />
      <Route path="/scan-product" element={<ProductScan />} />
      <Route path="/data" element={<ExportData/>} />
      {/* Add more routes as needed */}
    </Routes>
  );
}

export default App;

/*import React, { useRef, useState } from "react";
import "./App.css";
function App() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [name, setName] = useState("");
  const [message, setMessage] = useState("");

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (error) {
      console.error("Error accessing webcam:", error);
    }
  };

  const captureImage = () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    if (canvas && video) {
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      return canvas.toDataURL("image/jpeg");
    }
    return null;
  };

  const registerFace = async () => {
    const image = captureImage();
    if (!image || !name) {
      alert("Please enter a name and capture an image.");
      return;
    }

    const response = await fetch("http://127.0.0.1:5000/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, image }),
    });

    const data = await response.json();
    setMessage(data.message || data.error);
  };

  const identifyFace = async () => {
    const image = captureImage();
    if (!image) {
      alert("Please capture an image first.");
      return;
    }

    const response = await fetch("http://127.0.0.1:5000/identify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image }),
    });

    const data = await response.json();
    setMessage(data.identity || data.error);
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Face Recognition System</h1>
      <video ref={videoRef} autoPlay playsInline width="400" height="300"></video>
      <canvas ref={canvasRef} width="400" height="300" style={{ display: "none" }}></canvas>
      <div className="d1">
        <button onClick={startCamera} id="b1" className="btn btn-primary">Start Camera</button>
        <button onClick={registerFace}id="b2" className="btn">Register Face</button>
        <button onClick={identifyFace} id="b3" className="btn">Identify Face</button>
      </div>
      <div>
        <input type="text" placeholder="Enter Name" value={name} style={{borderRadius:"10px"}} onChange={(e) => setName(e.target.value)} />
      </div>
      <h2>{message}</h2>
    </div>
  );
}

export default App;
*/