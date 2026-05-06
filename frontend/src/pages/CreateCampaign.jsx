import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import "./CreateCampaign.css";
import { API_URL } from "../config";

export default function CreateCampaign() {
  const [form, setForm] = useState({
    campaign_name: "",
    description: "",
    reward_description: "",
    website_url: "",
    send_welcome_email : true,
  });
  // Protocol is tracked as separate state so the user gets a clean URL input
  // without having to type "https://". The backend's HttpUrl validator requires
  // a scheme, so we prepend it before submitting.
  const [protocol, setProtocol] = useState("https://");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({ ...prev, [name]: type === "checkbox" ? checked : value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Combine protocol + domain into a full URL before sending to the backend.
    // The backend uses this URL as the base for all referral links in this campaign.
    const payload = { ...form, website_url: protocol + form.website_url };
    const response = await fetch(`${API_URL}/campaigns`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      setError("Something went wrong. Please try again.");
    } else {
      navigate("/dashboard");
    }
  };

  return (
    <div className="cc-page">
      <Navbar />
      <main className="cc-main">
        <Link to="/dashboard" className="cc-back">← Back</Link>
        <div className="cc-card">
          <h2>Create Campaign</h2>
          <form className="cc-form" onSubmit={handleSubmit}>
            <div className="field">
              <label>Campaign Name</label>
              <input
                type="text"
                name="campaign_name"
                placeholder="e.g. Summer Referral Drive"
                value={form.campaign_name}
                onChange={handleChange}
              />
            </div>
            <div className="field">
              <label>What is the URL where you will host the campaign?</label>
              <div className="url-input">
                <select
                  className="url-protocol"
                  value={protocol}
                  onChange={(e) => setProtocol(e.target.value)}
                >
                  <option value="https://">https://</option>
                  <option value="http://">http://</option>
                </select>
                <div className="url-divider" />
                <input
                  type="text"
                  className="url-text"
                  name="website_url"
                  placeholder="yoursite.com/campaign"
                  value={form.website_url}
                  onChange={handleChange}
                />
              </div>
            </div>
            <div className="field">
              <label>Campaign Description <span className="field-optional">(optional)</span></label>
              <textarea
                name="description"
                placeholder="Short description of your campaign"
                value={form.description}
                onChange={handleChange}
              />
            </div>
            <div className="field">
              <label>Reward Description</label>
              <textarea
                name="reward_description"
                placeholder="e.g. $10 credit for every referral"
                value={form.reward_description}
                onChange={handleChange}
              />
            </div>
            <div className="field field-toggle">
              <label>Send Welcome Email</label>
              <label className="toggle">
                <input
                  type="checkbox"
                  name="sendWelcomeEmail"
                  checked={form.sendWelcomeEmail}
                  onChange={handleChange}
                />
                <span className="toggle-track">
                  <span className="toggle-thumb" />
                </span>
              </label>
            </div>
            <button type="submit" className="btn-submit">
              Create Campaign
            </button>
            {error && <p className="error">{error}</p>}
          </form>
        </div>
      </main>
      <Footer />
    </div>
  );
}
