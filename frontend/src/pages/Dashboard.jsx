import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import "./Dashboard.css";
import { useState, useEffect } from "react";
import { API_URL } from "../config";

export default function Dashboard() {
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [campaigns, setCampaigns] = useState([]);
  const [apiKey, setApiKey] = useState("");
  const [apiKeyCopied, setApiKeyCopied] = useState(false);

  useEffect(() => {
    const fetchCampaigns = async () => {
      // Check for a token before hitting the API so we don't make an
      // authenticated request that will fail — redirect immediately instead.
      // This is a client-side convenience check, not a security boundary;
      // the backend validates the token on every request.
      if (!localStorage.getItem("token")) {
        navigate("/login");
        return;
      }
      const response = await fetch(`${API_URL}/campaigns`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      if (!response.ok) {
        setError("Something broke");
      } else {
        const data = await response.json();
        setCampaigns(data.campaigns);
        setApiKey(data.api_key);
      }
    };
    fetchCampaigns();

    // API key is fetched separately from campaigns because /company/me is the
    // canonical source for account-level data, keeping campaign and company
    // concerns on distinct endpoints.
    const fetchApiKey = async () => {
      const response = await fetch(`${API_URL}/company/me`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setApiKey(data.api_key);
      }
    };
    fetchApiKey();
  }, []);
  return (
    <div className="dashboard-page">
      <Navbar />
      <main className="dashboard-main">
        {campaigns.length === 0 ? (
          <div className="empty-state">
            <button
              className="btn-create"
              onClick={() => navigate("/create-campaign")}
            >
              <span className="btn-create-icon">+</span>
              Create Campaign
            </button>
            <p className="empty-subtext">Create your first campaign.</p>
          </div>
        ) : (
          <div className="campaigns-view">
            <div className="campaigns-header">
              <h2 className="campaigns-heading">Campaigns</h2>
              <button
                className="btn-create"
                onClick={() => navigate("/create-campaign")}
              >
                <span className="btn-create-icon">+</span>
                Create Campaign
              </button>
            </div>
            <div className="campaigns-list">
              {campaigns.map((campaign) => (
                <div key={campaign.id} className="campaign-card">
                  <span className="campaign-name">
                    {campaign.campaign_name}
                  </span>
                  <button
                    className="btn-view"
                    onClick={() => navigate(`/campaigns/${campaign.id}`)}
                  >
                    View
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
        <div className="apikey-section">
          <span className="apikey-label">Your API Key</span>
          <div className="apikey-row">
            <span className="apikey-value">{apiKey || "—"}</span>
            <button
              className="btn-copy-key"
              onClick={() => {
                navigator.clipboard.writeText(apiKey);
                setApiKeyCopied(true);
                // Reset label after 2 seconds — long enough to read "Copied!"
                // but short enough that the button doesn't stay disabled-looking.
                setTimeout(() => setApiKeyCopied(false), 2000);
              }}
            >
              {apiKeyCopied ? "Copied!" : "Copy"}
            </button>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
