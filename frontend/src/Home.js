import React, { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./App.css";

function Home() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [name, setName] = useState("");
  const [message, setMessage] = useState("");
  const [rfid, setRfid] = useState("");
  const [isFaceRegistered, setIsFaceRegistered] = useState(false);
  const [isRFIDRegistered, setIsRFIDRegistered] = useState(false);
  const navigate = useNavigate();

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
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      return canvas.toDataURL("image/jpeg");
    }
    return null;
  };

  const registerFace = async () => {
    if (!name) {
      alert("Please enter your name first.");
      return;
    }

    const image = captureImage();
    if (!image) {
      alert("Please capture an image first.");
      return;
    }

    const response = await fetch("http://127.0.0.1:5000/register_face", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, image }),
    });

    const data = await response.json();
    setMessage(data.message || data.error);
    if (data.message) setIsFaceRegistered(true);
  };

  const fetchRFID = async () => {
    if (!isFaceRegistered) {
      alert("Please register your face first.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/get_rfid");
      const data = await response.json();
      console.log("RFID Response:", data);
      if (data.rfid) {
        setRfid(data.rfid);
        setIsRFIDRegistered(true);

        await fetch("http://127.0.0.1:5000/register_rfid", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name, rfid: data.rfid }),
        });
        setMessage("RFID registered successfully!");
      }
    } catch (error) {
      console.error("Error fetching RFID:", error);
      setRfid("Error fetching RFID");
    }
  };

  const identifyFace = async () => {
    if (!isFaceRegistered || !isRFIDRegistered) {
      alert("Please complete both face and RFID registration before identification.");
      return;
    }

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
      <div className="a1">
        <h1>Face & RFID Recognition</h1>
        <video ref={videoRef} autoPlay playsInline width="400" height="300"></video>
        <canvas ref={canvasRef} width="400" height="300" style={{ display: "none" }}></canvas>
        <div className="d1">
          <button onClick={startCamera} className="btn btn-primary" style={{background:"yellow",color:"white"}} id="b2">
            Start Camera
          </button>
          <button onClick={registerFace} className="btn" id="b3">
            Register Face
          </button>
          <button onClick={fetchRFID} className="btn btn-secondary" id="b5">
            Tap RFID Card
          </button>
          <button onClick={identifyFace} className="btn btn-secondary" id="b4">
            Identify Face
          </button>
        </div>
      </div>
      <div>
        <input
          type="text"
          placeholder="Enter Name"
          value={name}
          style={{ borderRadius: "10px" }}
          onChange={(e) => setName(e.target.value)}
        />
      </div>
      <h2>{message}</h2>
      <div className="c1">
        <h2>RFID: {rfid}</h2>
        {rfid && (
          <button onClick={() => navigate("/scan-product")} className="btn btn-secondary">
            Proceed to Product Scanning
          </button>
        )}
      </div>
    </div>
  );
}

export default Home;


//RECENT-CODE
/*import React, { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./App.css";

function Home() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [name, setName] = useState("");
  const [message, setMessage] = useState("");
  const [rfid, setRfid] = useState("");
  const [isFaceRegistered, setIsFaceRegistered] = useState(false);
  const [isRFIDRegistered, setIsRFIDRegistered] = useState(false);
  const navigate = useNavigate();

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
      ctx.fillRect(0, 0, canvas.width, canvas.height);
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

    const response = await fetch("http://127.0.0.1:5000/register_face", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, image }),
    });

    const data = await response.json();
    setMessage(data.message || data.error);
    if (data.message) setIsFaceRegistered(true);
  };

  const fetchRFID = async () => {
    if (!isFaceRegistered) {
      alert("Please register your face first.");
      return;
    }
    try {
      const response = await fetch("http://127.0.0.1:5000/get_rfid");
      const data = await response.json();
      console.log("RFID Response:", data);
      if (data.rfid) {
        setRfid(data.rfid);
        setIsRFIDRegistered(true);

        await fetch("http://127.0.0.1:5000/register_rfid", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name, rfid: data.rfid }),
        });
        setMessage("RFID registered successfully!");
      }
    } catch (error) {
      console.error("Error fetching RFID:", error);
      setRfid("Error fetching RFID");
    }
  };

  const identifyFace = async () => {
    if (!isRFIDRegistered) {
      alert("Please register your RFID first.");
      return;
    }

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
      <div className="a1">
        <h1>Face & RFID Recognition</h1>
        <video ref={videoRef} autoPlay playsInline width="400" height="300"></video>
        <canvas ref={canvasRef} width="400" height="300" style={{ display: "none" }}></canvas>
        <div className="d1">
          <button onClick={startCamera} className="btn btn-primary" id="b2">Start Camera</button>
          <button onClick={registerFace} className="btn" id="b3">Register Face</button>
          <button onClick={fetchRFID} className="btn btn-secondary" id="b5">Tap RFID Card</button>
          <button onClick={identifyFace} className="btn btn-secondary" id="b4">Identify Face</button>
        </div>
      </div>
      <div>
        <input type="text" placeholder="Enter Name" value={name} style={{ borderRadius: "10px" }} onChange={(e) => setName(e.target.value)} />
      </div>
      <h2>{message}</h2>
      <div className="c1">
        <h2>RFID: {rfid}</h2>
        {rfid && <button onClick={() => navigate("/scan-product")} className="btn btn-secondary">Proceed to Product Scanning</button>}
      </div>
    </div>
  );
}

export default Home;
*/


//OLD-CODE:Use only in case of emergency

/*import React, { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./App.css";

function Home() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [name, setName] = useState("");
  const [message, setMessage] = useState("");
  const [rfid, setRfid] = useState("");
  const navigate = useNavigate();

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
      ctx.fillRect(0, 0, canvas.width, canvas.height);
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

    const response = await fetch("http://127.0.0.1:5000/register_face", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, image }),
    });

    const data = await response.json();
    setMessage(data.message || data.error);
  };

  const fetchRFID = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/get_rfid");
      const data = await response.json();
      console.log("RFID Response:", data);
      setRfid(data.rfid || "RFID not detected");
    } catch (error) {
      console.error("Error fetching RFID:", error);
      setRfid("Error fetching RFID");
    }
  };

  const identifyFace = async () => {
    if (!rfid) {
      alert("Please scan your RFID first.");
      return;
    }

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
      <div className="a1">
        <h1>Face & RFID Recognition</h1>
        <video ref={videoRef} autoPlay playsInline width="400" height="300"></video>
        <canvas ref={canvasRef} width="400" height="300" style={{ display: "none" }}></canvas>
        <div className="d1">
          <button onClick={startCamera} className="btn btn-primary" id="b2">Start Camera</button>
          <button onClick={registerFace} className="btn" id="b3">Register Face</button>
          <button onClick={identifyFace} className="btn btn-secondary" id="b4">Identify Face</button>
        </div>
      </div>
      <div>
        <input type="text" placeholder="Enter Name" value={name} style={{ borderRadius: "10px" }} onChange={(e) => setName(e.target.value)} />
      </div>
      <h2>{message}</h2>
      <div className="c1">
        <h2>RFID: {rfid}</h2>
        <button onClick={fetchRFID} className="btn btn-primary">Tap RFID Card</button>
        {rfid && <button onClick={() => navigate("/scan-product")} className="btn btn-secondary">Proceed to Product Scanning</button>}
      </div>
    </div>
  );
}

export default Home;
*/