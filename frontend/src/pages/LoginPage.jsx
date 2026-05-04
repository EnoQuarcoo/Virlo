import { Link, useNavigate } from "react-router-dom";
import "./LoginPage.css";
import { useState } from "react";

export default function LoginPage() {
  //Create log in variables
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    //update the email and password
    e.preventDefault();
    const response = await fetch("http://127.0.0.1:8000/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });
    if (!response.ok) {
      console.log("Something went wrong");
      const data = await response.json();
      setError("Invalid email or password")
    } else {
      const data = await response.json();
      localStorage.setItem("token", data.token);
      navigate("/dashboard");
    }
  };
  return (
    <div className="login-page">
      <nav className="login-nav">
        <Link to="/" className="nav-logo">
          Virlo
        </Link>
      </nav>
      <div className="login-wrap">
        <div className="login-card">
          <h2>Welcome back</h2>
          <p>Sign in to your Virlo account</p>
          <form className="login-form" onSubmit={handleSubmit}>
            <div className="field">
              <label>Email</label>
              <input
                type="email"
                placeholder="you@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="field">
              <label>Password</label>
              <input
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            {error && <p className="error">{error}</p>}
            <button type="submit" className="btn-submit">
              Sign In
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
