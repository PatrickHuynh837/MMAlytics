// client/src/pages/Events.tsx
import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";

interface Event {
  event_url?: string;
  event_name: string;
  event_date: string;
  location_city?: string;
  location_state?: string;
  location_country?: string;
}

function Events() {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchEvents() {
      try {
        setLoading(true);
        const res = await fetch("/api/events");
        if (!res.ok) {
          throw new Error(`Failed to fetch events (Status: ${res.status})`);
        }
        const data: Event[] = await res.json();
        setEvents(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
      } finally {
        setLoading(false);
      }
    }

    fetchEvents();
  }, []);

  return (
    <div>
      <Navbar />
      <h1>UFC Events</h1>

      {loading && <p>Loading events...</p>}
      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      {!loading && !error && (
        <div className="events-grid">
          {events.map((event, idx) => (
            <div key={event.event_url || idx} className="event-card">
              <h3>{event.event_name}</h3>
              <p>📅 {event.event_date}</p>
              <p>
                📍 {[event.location_city, event.location_state, event.location_country]
                  .filter(Boolean)
                  .join(", ")}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Events;
