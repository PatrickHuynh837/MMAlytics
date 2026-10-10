
import { useState } from "react";
import Navbar from "../components/Navbar";

type AnalyticsView =
  | "performance"
  | "trajectories"
  | "styles"
  | "similarity"
  | "matchups"
  | "divisions";

function Analytics() {
  const [activeView, setActiveView] =
    useState<AnalyticsView>("performance");

  const views: { id: AnalyticsView; label: string }[] = [
    { id: "performance", label: "Performance" },
    { id: "trajectories", label: "Trajectories" },
    { id: "styles", label: "Style Analysis" },
    { id: "similarity", label: "Fighter Similarity" },
    { id: "matchups", label: "Matchup Analysis" },
    { id: "divisions", label: "Division Analytics" },
  ];

  return (
    <div>
      <Navbar />

      <h1>Analytics</h1>

      <div>
        {views.map((view) => (
          <button
            key={view.id}
            onClick={() => setActiveView(view.id)}
            aria-pressed={activeView === view.id}
          >
            {view.label}
          </button>
        ))}
      </div>

      <div>
        {activeView === "performance" && (
          <section>
            <h2>Fighter Performance</h2>
            <p>
              Analyze historical fighter statistics and performance trends.
            </p>
          </section>
        )}

        {activeView === "trajectories" && (
          <section>
            <h2>Fighter Trajectories</h2>
            <p>
              Explore how fighter performance changes throughout a career.
            </p>
          </section>
        )}

        {activeView === "styles" && (
          <section>
            <h2>Style Analysis</h2>
            <p>
              Explore fighter styles and statistically similar archetypes.
            </p>
          </section>
        )}

        {activeView === "similarity" && (
          <section>
            <h2>Fighter Similarity</h2>
            <p>
              Identify fighters with similar statistical profiles.
            </p>
          </section>
        )}

        {activeView === "matchups" && (
          <section>
            <h2>Matchup Analysis</h2>
            <p>
              Compare fighter characteristics and potential matchup advantages.
            </p>
          </section>
        )}

        {activeView === "divisions" && (
          <section>
            <h2>Division Analytics</h2>
            <p>
              Explore historical trends and performance across divisions.
            </p>
          </section>
        )}
      </div>
    </div>
  );
}

export default Analytics;

