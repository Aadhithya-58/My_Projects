import {React} from 'react';
import "./App.css";
import { useNavigate} from 'react-router-dom';
function Homepage() {
    const navigate=useNavigate();
    return (
    <div className="topclass">
        <h1 className="text-center">Lab components lending system</h1>
        <div className="header">
            <div className="login">
                <h2>Login</h2><br/><br/>
                <button id="l1" className="btn" onClick={()=>navigate("/data")}>Login for Admin</button><br/>
                <button id="l2" className="btn" onClick={()=>navigate("/home")}>Login for Students</button><br/>
            </div>
        </div>
    </div>
  );
}

export default Homepage;