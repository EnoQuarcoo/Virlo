import { Link } from "react-router-dom";
import "./SignupPage.css";
import { useState } from "react";
import { useNavigate } from "react-router";
import { API_URL } from "../config";


export default function SignupPage() {
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate()


  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    // Only clear the error when the user edits email or password — those are
    // the fields that cause auth errors. The company name field is optional and
    // doesn't trigger validation errors, so clearing on name change would be
    // misleading.
    if (name === "email" || name === "password") {
      setError("");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch(`${API_URL}/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(form),
    });

    if (!response.ok) {
      setError("Something went wrong. Please try again");
    } else {
      // The backend returns a JWT immediately after registration, so we store
      // it and navigate to the dashboard — no separate login step needed.
      const data = await response.json();
      localStorage.setItem("token", data.token);
      navigate("/dashboard");
    }
  };

  return (
    <div className="signup-page">
      <nav className="signup-nav">
        <Link to="/" className="nav-logo">Virlo</Link>
      </nav>
      <div className="signup-wrap">
        <div className="signup-card">
          <h2>Create your account</h2>
          <p>Start your referral program today</p>
          <form className="signup-form" onSubmit={handleSubmit}>
            <div className="field">
              <label>Company Name</label>
              <input
                type="text"
                name="name"
                placeholder="Acme Inc."
                value={form.name}
                onChange={handleChange}
              />
            </div>
            <div className="field">
              <label>Email</label>
              <input
                type="email"
                name="email"
                placeholder="you@company.com"
                value={form.email}
                onChange={handleChange}
              />
            </div>
            <div className="field">
              <label>Password</label>
              <input
                type="password"
                name="password"
                placeholder="••••••••"
                value={form.password}
                onChange={handleChange}
              />
            </div>
            <button type="submit" className="btn-submit">
              Create Account
            </button>
          </form>
          <p className="auth-switch">
            Already have an account?{" "}
            <Link to="/login" className="auth-switch-link">Login</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
