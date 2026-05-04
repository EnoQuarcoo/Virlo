import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import "./Dashboard.css";

export default function Dashboard() {
  const navigate = useNavigate();

  return (
    <div className="dashboard-page">
      <Navbar />
      <main className="dashboard-main">
        <div className="empty-state">
          <button className="btn-create" onClick={() => navigate("/create-campaign")}>
            <span className="btn-create-icon">+</span>
            Create Campaign
          </button>
          <p className="empty-subtext">Create your first campaign.</p>
        </div>
      </main>
      <Footer />
    </div>
  );
}
