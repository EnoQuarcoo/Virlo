import { Link, useNavigate } from "react-router-dom";
import "./LoginPage.css";
import { useState } from "react";
import { API_URL } from "../config";

export default function LoginPage() {
  //Create log in variables
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });
    if (!response.ok) {
      console.log("Something went wrong");
      const data = await response.json();
      // Show the same message regardless of whether the email or password was
      // wrong, matching the backend's intentionally generic error response to
      // prevent email enumeration attacks.
      setError("Invalid email or password");
    } else {
      const data = await response.json();
      // JWT is stored in localStorage rather than a cookie so it persists
      // across browser tabs and page refreshes without requiring server-side
      // session management.
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
          {/* Clear the error as soon as the user edits either field so stale
              error messages don't linger after they've corrected their input. */}
          <form className="login-form" onSubmit={handleSubmit}>
            <div className="field">
              <label>Email</label>
              <input
                type="email"
                placeholder="you@company.com"
                value={email}
                onChange={(e) => {setEmail(e.target.value); setError("");}}
              />
            </div>
            <div className="field">
              <label>Password</label>
              <input
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => {setPassword(e.target.value); setError("");}}
              />
            </div>
            {error && <p className="error">{error}</p>}
            <button type="submit" className="btn-submit">
              Sign In
            </button>
          </form>
          <p className="auth-switch">
            Don't have an account?{" "}
            <Link to="/signup" className="auth-switch-link">Sign up</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
