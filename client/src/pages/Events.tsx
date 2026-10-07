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
  // Stores all events returned by the backend
  const [events, setEvents] = useState<Event[]>([]);

  // Tracks whether the API request is still loading
  const [loading, setLoading] = useState<boolean>(true);

  // Stores an error message if the API request fails
  const [error, setError] = useState<string | null>(null);

  // Number of events displayed on each page
  const EVENTS_PER_PAGE = 30;

  // Tracks which pagination page the user is currently viewing
  const [currentPage, setCurrentPage] = useState<number>(1);

  // Fetch events from the FastAPI backend
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

  // Calculate how many pages are needed
  const totalPages = Math.ceil(
    events.length / EVENTS_PER_PAGE
  );

  // Calculate where the current page starts in the events array
  const startIndex =
    (currentPage - 1) * EVENTS_PER_PAGE;

  // Only display the 30 events belonging to the current page
  const currentEvents = events.slice(
    startIndex,
    startIndex + EVENTS_PER_PAGE
  );

  return (
    <div>
      <Navbar />

      <h1>UFC Events</h1>

      {/* Display loading message while waiting for the API */}
      {loading && <p>Loading events...</p>}

      {/* Display error message if the API request fails */}
      {error && (
        <p style={{ color: "red" }}>
          Error: {error}
        </p>
      )}

      {/* Display events after they have successfully loaded */}
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

          {/* Pagination buttons */}
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
  );
}

export default Events;
