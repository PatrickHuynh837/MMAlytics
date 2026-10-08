
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

const EVENTS_PER_PAGE = 30;

// Extract the UFCStats event ID from the event URL.
function getEventId(eventUrl: string): string {
  return eventUrl.split("/").pop() ?? "";
}

function Events() {
  const [events, setEvents] = useState<Event[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchEvents() {
      try {
        const response = await fetch("http://127.0.0.1:8000/events");

        if (!response.ok) {
          throw new Error(
            `Failed to fetch events (Status: ${response.status})`
          );
        }

        const data: Event[] = await response.json();
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

  const currentEvents = events.slice(
    startIndex,
    startIndex + EVENTS_PER_PAGE
  );

  return (
    <div className="events-page-container">
      <Navbar />

      <div className="events-content">
        <h1>UFC Events</h1>

        {loading && (
          <p className="status-message">
            Loading events...
          </p>
        )}

        {error && (
          <p className="status-message error-message">
            Error: {error}
          </p>
        )}

        {!loading && !error && (
          <>
            <div className="events-grid">
              {currentEvents.map((event, index) => {
                const eventId = getEventId(event.event_url ?? "");

                const location = [
                  event.location_city,
                  event.location_state,
                  event.location_country,
                ]
                  .filter(Boolean)
                  .join(", ");

                return (
                  <Link
                    key={event.event_url ?? index}
                    to={`/events/${eventId}`}
                    className="event-card"
                  >
                    <h3>{event.event_name}</h3>

                    <p>📅 {event.event_date}</p>

                    <p>📍 {location}</p>
                  </Link>
                );
              })}
            </div>

            <div className="pagination">
              {Array.from({ length: totalPages }, (_, index) => {
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
              })}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default Events;

