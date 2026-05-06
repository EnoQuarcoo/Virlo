import { Link, useNavigate } from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    // JWTs are stateless — there's no server-side session to invalidate.
    // Removing the token from localStorage is the only logout mechanism:
    // once it's gone, the client can't make authenticated requests.
    localStorage.removeItem("token");
    // Navigate to the landing page rather than /login so the user lands on a
    // welcoming page instead of being immediately prompted to sign back in.
    navigate("/");
  };

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-logo">Virlo</Link>
      <button className="navbar-logout" onClick={handleLogout}>Logout</button>
    </nav>
  );
}
