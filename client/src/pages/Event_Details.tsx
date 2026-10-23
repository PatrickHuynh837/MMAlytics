import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import Navbar from "../components/Navbar";

interface Fight {
fight_url: string;
fighter_1: string;
fighter_2: string;
weight_class: string;
}

function getFightId(fightUrl: string): string {
return fightUrl.split("/").pop() ?? "";
}

function EventDetails() {
const { eventId } = useParams<{ eventId: string }>();

const eventUrl = eventId
? `http://ufcstats.com/event-details/${eventId}`
: undefined;

const [fights, setFights] = useState<Fight[]>([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState<string | null>(null);

useEffect(() => {
async function fetchFights() {
setLoading(true);
setError(null);
setFights([]);


  console.log("Event ID:", eventId);
  console.log("Event URL:", eventUrl);

  if (!eventUrl) {
    setError("Event URL not found. Please return to the events page.");
    setLoading(false);
    return;
  }

  try {
    const apiUrl =
      `http://127.0.0.1:8000/fights/?event_url=${encodeURIComponent(eventUrl)}`;

    console.log("Fetching fights from:", apiUrl);

    const response = await fetch(apiUrl);

    console.log("Response status:", response.status);

    if (!response.ok) {
      throw new Error(
        `Failed to fetch fights (Status: ${response.status})`
      );
    }

    const data: Fight[] = await response.json();

    console.log("Fights received from API:", data);
    console.log("Number of fights:", data.length);

    setFights(data);
  } catch (err) {
    console.error("Error fetching fights:", err);

    setError(
      err instanceof Error ? err.message : "Unknown error"
    );
  } finally {
    setLoading(false);
  }
}

fetchFights();


}, [eventId, eventUrl]);

return ( <div className="events-page-container"> <Navbar />


  <div className="events-content">
    <h1>Event Fight Card</h1>

    {loading && (
      <p className="status-message">Loading fights...</p>
    )}

    {error && (
      <p className="status-message error-message">
        Error: {error}
      </p>
    )}

    {!loading && !error && fights.length === 0 && (
      <p>No fights found for this event.</p>
    )}

    {!loading && !error && fights.length > 0 && (
      <div className="events-grid">
        {fights.map((fight) => {
          const fightId = getFightId(fight.fight_url);

          return (
            <Link
              key={fight.fight_url}
              to={`/fights/${encodeURIComponent(fightId)}`}
              state={{ fightUrl: fight.fight_url }}
              className="event-card"
            >
              <h3>
                {fight.fighter_1} vs. {fight.fighter_2}
              </h3>

              <p>{fight.weight_class}</p>
            </Link>
          );
        })}
      </div>
    )}

    <Link to="/events" className="back-link">
      Back to Events
    </Link>
  </div>
</div>


);
}

export default EventDetails;
