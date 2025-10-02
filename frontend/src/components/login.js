import React, { useState } from "react";
import "../pages/Login.css";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    if (!username || !password) {
      setErrorMessage("Please enter username and password");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/token/", {
        username: username,
        password: password,
      });

      if (response.status === 200) {
        console.log("Login success:", response.data);

        // if backend returns token (DRF TokenAuth)
        if (response.data.token) {
          localStorage.setItem("token", response.data.token);
        }

        // if backend returns JWT tokens (SimpleJWT)
        if (response.data.access) {
          localStorage.setItem("access", response.data.access);
          localStorage.setItem("refresh", response.data.refresh);
        }

        navigate("/dashboard"); // redirect to dashboard
      }
    } catch (error) {
      console.error("Login error:", error);
      if (error.response && error.response.data) {
        setErrorMessage(error.response.data.detail || "Login failed");
      } else {
        setErrorMessage("Login failed. Please try again.");
      }
    }
  };

  return (
    <div className="container mt-4">
      <div className="card">
        <h2 className="heading">Login</h2>

        {errorMessage && <div className="alert alert-danger">{errorMessage}</div>}

        <form onSubmit={handleLogin}>
          <div className="field">
            <input
              className="form-control mb-3"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className="field">
            <input
              className="form-control mb-2 mt-4"
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <div>
            <button type="submit" className="btn btn-primary float-right">
              Login
            </button>
          </div>
        </form>

        <p className="mt-3">
          Don’t have an account? <Link to="/register">Sign Up</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;
