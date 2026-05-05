import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import "./Dashboard.css";
import { useState, useEffect } from "react";

export default function Dashboard() {
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [campaigns, setCampaigns] = useState([])

  useEffect(() => {
    const fetchCampaigns = async () => {
      const response = await fetch("http://127.0.0.1:8000/campaigns", {
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
        // store the campaigns in state here
        setCampaigns(data.campaigns)
        console.log(data.campaigns)
      }
    };
    fetchCampaigns();
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
                  <span className="campaign-name">{campaign.campaign_name}</span>
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
       </main>
      <Footer />
    </div>
  );
}
