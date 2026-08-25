import { Link } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <Link to="/">Home</Link>
      <Link to="/dashboard">Dashboard</Link>
      <Link to="/analytics">Analytics</Link>
      <Link to="/events">Events</Link>
      <Link to="/fighters">Fighters</Link>
      <Link to="/matchup">Matchup</Link>
      <Link to="/prediction">Prediction</Link>
      <Link to="/comparison">Comparison</Link>
    </nav>
  );
}

export default Navbar;