import { Link } from "react-router-dom";
import "./Footer.css";

export default function Footer() {
  return (
    <footer className="footer">
      <span className="footer-brand">Virlo</span>
      <div className="footer-links">
        <a href="https://virlo.mintlify.app" target="_blank" rel="noreferrer">Documentation</a>
        <Link to="/terms">Terms</Link>
        <Link to="/privacy">Privacy</Link>
      </div>
    </footer>
  );
}
