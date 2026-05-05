import { Link, useNavigate } from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-logo">Virlo</Link>
      <button className="navbar-logout" onClick={handleLogout}>Logout</button>
    </nav>
  );
}
