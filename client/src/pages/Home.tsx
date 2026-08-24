import { Link } from "react-router-dom";

function Home() {
  return (
    <>
      <h1>Welcome to MMAlytics</h1>

      <Link to="/dashboard">Dashboard</Link>
      <Link to="/analytics">Analytics</Link>
      <Link to="/events">Events</Link>
      <Link to="/fighters">Fighters</Link>
      <Link to="/matchup">Matchup</Link>
      <Link to="/prediction">Prediction</Link>
      <Link to="/comparison">Comparison</Link>
    </>
  );
}

export default Home;