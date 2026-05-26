import { useState, useEffect } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import "./CampaignDetail.css";
import { API_URL } from "../config";

export default function CampaignDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [leaderboard, setLeaderboard] = useState([]);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(null);
  const [campaignIDCopied, setCampaignIDCopied] = useState(false);
  const location = useLocation();
  // Populated by navigate() in Dashboard — avoids a second API call just for
  // the campaign name and ID. Will be null if the user navigates directly to this URL.
  const campaignData = location.state

  // Re-runs if the campaign id in the URL changes (e.g. back/forward navigation).
  useEffect(() => {
    const fetchLeaderboard = async () => {
      const response = await fetch(`${API_URL}/campaigns/${id}/leaderboard`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      if (!response.ok) {
        setError("Failed to load leaderboard.");
      } else {
        const data = await response.json();
        setLeaderboard(data.leaderboard);
      }
    };
    fetchLeaderboard();
  }, [id]);

  const handleCopy = (link, index) => {
    navigator.clipboard.writeText(link);
    // Track which row was copied by index rather than a boolean so multiple
    // "Copy" buttons can each show "Copied!" independently without interfering.
    setCopied(index);
    setTimeout(() => setCopied(null), 2000);
  };

  return (
    <div className="cd-page">
      <Navbar />
      <main className="cd-main">
        <button
          className="cd-back"
          onClick={() => {
            navigate("/dashboard");
          }}
        >
          ← Back
        </button>
        {error ? (
          <p className="cd-error">{error}</p>
        ) : (
          <>
            <h1 className="cd-title">{campaignData?.campaignName}</h1>
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
                  {/* The backend already sorts by referral_count DESC, so
                      index maps directly to rank — no client-side sort needed. */}
                  {leaderboard.map((entry, index) => (
                    <tr key={index}>
                      <td className="cd-rank">{index + 1}</td>
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
            {/* Campaign ID displayed here so the user can copy it for use with the public signup API. */}
            <div className="apikey-section">
              <span className="apikey-label">Campaign ID</span>
              <div className="apikey-row">
                <span className="apikey-value">{campaignData?.campaignID || "—"}</span>
                <button
                  className="btn-copy-key"
                  onClick={() => {
                    navigator.clipboard.writeText(String( campaignData?.campaignID));
                    setCampaignIDCopied(true);
                    setTimeout(() => setCampaignIDCopied(false), 2000);
                  }}
                >
                  {campaignIDCopied ? "Copied!" : "Copy"}
                </button>
              </div>
            </div>
          </>
        )}
      </main>
      <Footer />
    </div>
  );
}
