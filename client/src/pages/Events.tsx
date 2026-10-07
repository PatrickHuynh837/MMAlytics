import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
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

  const EVENTS_PER_PAGE = 30;
  const [currentPage, setCurrentPage] = useState<number>(1);

  useEffect(() => {
    async function fetchEvents() {
      try {
        setLoading(true);
        const res = await fetch("http://127.0.0.1:8000/events");

        if (!res.ok) {
          throw new Error(
            `Failed to fetch events (Status: ${res.status})`
          );
        }

        const data: Event[] = await res.json();
        setEvents(data);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Unknown error"
        );
      } finally {
        setLoading(false);
      }
    }

    fetchEvents();
  }, []);

  const totalPages = Math.ceil(events.length / EVENTS_PER_PAGE);
  const startIndex = (currentPage - 1) * EVENTS_PER_PAGE;
  const currentEvents = events.slice(startIndex, startIndex + EVENTS_PER_PAGE);

  return (
    <div className="events-page-container">
      <Navbar />

      <div className="events-content">
        <h1>UFC Events</h1>

        {loading && <p className="status-message">Loading events...</p>}

        {error && (
          <p className="status-message error-message">
            Error: {error}
          </p>
        )}

        {!loading && !error && (
          <>
            <div className="events-grid">
              {currentEvents.map((event, idx) => (
                <Link
                  key={event.event_url || idx}
                  to={`/events/${encodeURIComponent(
                    event.event_url ?? ""
                  )}`}
                  className="event-card"
                >
                  <h3>{event.event_name}</h3>
                  <p>📅 {event.event_date}</p>
                  <p>
                    📍{" "}
                    {[
                      event.location_city,
                      event.location_state,
                      event.location_country,
                    ]
                      .filter(Boolean)
                      .join(", ")}
                  </p>
                </Link>
              ))}
            </div>

            <div className="pagination">
              {Array.from(
                { length: totalPages },
                (_, index) => {
                  const page = index + 1;
                  return (
                    <button
                      key={page}
                      onClick={() => setCurrentPage(page)}
                      disabled={currentPage === page}
                    >
                      {page}
                    </button>
                  );
                }
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default Events;