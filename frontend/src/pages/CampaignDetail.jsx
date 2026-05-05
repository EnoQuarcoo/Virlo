import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import "./CampaignDetail.css";

export default function CampaignDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [campaignName, setCampaignName] = useState("");
  const [leaderboard, setLeaderboard] = useState([]);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(null);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      const response = await fetch(
        `http://127.0.0.1:8000/campaigns/${id}/leaderboard`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      if (!response.ok) {
        setError("Failed to load leaderboard.");
      } else {
        const data = await response.json();
        setCampaignName(data.campaign_name);
        setLeaderboard(data.leaderboard);
      }
    };
    fetchLeaderboard();
  }, [id]);

  const handleCopy = (link, index) => {
    navigator.clipboard.writeText(link);
    setCopied(index);
    setTimeout(() => setCopied(null), 2000);
  };

  return (
    <div className="cd-page">
      <Navbar />
      <main className="cd-main">
        <button className="cd-back" onClick={() => navigate("/dashboard")}>
          ← Back
        </button>
        {error ? (
          <p className="cd-error">{error}</p>
        ) : (
          <>
            <h1 className="cd-title">{campaignName}</h1>
            <div className="cd-card">
              <table className="cd-table">
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Email</th>
                    <th>Referral Link</th>
                    <th>Referral Count</th>
                  </tr>
                </thead>
                <tbody>
                  {leaderboard.map((entry, index) => (
                    <tr key={index}>
                      <td className="cd-rank">{entry.rank}</td>
                      <td>{entry.email}</td>
                      <td className="cd-link-cell">
                        <span className="cd-link">{entry.referral_link}</span>
                        <button
                          className="btn-copy"
                          onClick={() => handleCopy(entry.referral_link, index)}
                        >
                          {copied === index ? "Copied!" : "Copy"}
                        </button>
                      </td>
                      <td className="cd-count">{entry.referral_count}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}
      </main>
      <Footer />
    </div>
  );
}
