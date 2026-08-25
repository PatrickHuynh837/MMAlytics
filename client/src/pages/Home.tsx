import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import "./styles/Home.css";

const features = [
  {
    title: "Explore UFC Fighters",
    description: "Discover fighter records, performance stats, strengths, and historical trends.",
    link: "/fighters",
  },
  {
    title: "Compare Matchups",
    description: "Compare two fighters across striking, grappling, experience, and physical attributes.",
    link: "/matchup",
  },
  {
    title: "Upcoming Fights",
    description: "Browse upcoming UFC events and explore scheduled fight cards.",
    link: "/events",
  },
  {
    title: "Fight Predictions",
    description: "Explore model-based predictions and evaluate fight outcomes with historical data.",
    link: "/prediction",
  },
  {
    title: "Historical Analytics",
    description: "Dive deep into UFC statistics and trends across fighters and divisions over time.",
    link: "/analytics",
  },
];

function Home() {
  return (
    <div className="home-container">
      <h1>Welcome to MMAlytics</h1>
      <Navbar />

      {/* Hero Section */}
      <section className="hero-section">
        <h2>Understand the Fight Before It Starts</h2>
        <p className="hero-subtitle">
          MMAlytics is a UFC analytics platform built to help fans explore
          fighters, matchups, events, and fight predictions.
        </p>
      </section>

      {/* Feature Cards Grid */}
      <div className="features-grid">
        {features.map((item) => (
          <Link to={item.link} key={item.title} className="feature-card">
            <h3>{item.title}</h3>
            <p>{item.description}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}

export default Home;
