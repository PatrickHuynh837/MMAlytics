import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";

interface Fighter {
  fighter_url?: string;
  fighter_name: string;
  fighter_nickname?: string;
  fighter_height_cm?: number;
  fighter_weight_lbs?: number;
  fighter_reach_cm?: number;
  fighter_stance?: string;
  fighter_w?: number;
  fighter_l?: number;
  fighter_d?: number;
}

function FighterProfile() {
  const [fighters, setFighters] = useState<Fighter[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchFighters() {
      try {
        setLoading(true);

        const res = await fetch("http://127.0.0.1:8000/fighters");

        if (!res.ok) {
          throw new Error(
            `Failed to fetch fighters (Status: ${res.status})`
          );
        }

        const data: Fighter[] = await res.json();
        setFighters(data);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Unknown error"
        );
      } finally {
        setLoading(false);
      }
    }

    fetchFighters();
  }, []);

  return (
    <div>
      <Navbar />

      <h1>Fighters</h1>

      {loading && <p>Loading fighters...</p>}

      {error && (
        <p style={{ color: "red" }}>
          Error: {error}
        </p>
      )}

      {!loading && !error && (
        <div className="events-grid">
          {fighters.map((fighter, idx) => (
            <div
              key={fighter.fighter_url || idx}
              className="event-card"
            >
              <h3>
                {fighter.fighter_name}{" "}
                {fighter.fighter_nickname &&
                  `"${fighter.fighter_nickname}"`}
              </h3>

              <p>
                Record: {fighter.fighter_w}-{fighter.fighter_l}-
                {fighter.fighter_d}
              </p>

              <p>
                Height: {fighter.fighter_height_cm} cm
              </p>

              <p>
                Weight: {fighter.fighter_weight_lbs} lbs
              </p>

              <p>
                Reach: {fighter.fighter_reach_cm} cm
              </p>

              <p>
                Stance: {fighter.fighter_stance}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default FighterProfile;