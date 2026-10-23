
import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import Navbar from "../components/Navbar";

interface FightDetailsData {
  fight_url: string;
  event_name: string | null;
  referee: string | null;
  fighter_1: string | null;
  fighter_2: string | null;
  fighter_1_url: string | null;
  fighter_2_url: string | null;
  winner: string | null;
  num_rounds: number | null;
  title_fight: boolean | null;
  gender: string | null;
  result: string | null;
  result_details: string | null;
  finish_round: number | null;
  finish_time: string | null;
  weight_class: string | null;

  fighter_1_knockdowns: number | null;
  fighter_1_total_strikes_att: number | null;
  fighter_1_total_strikes_succ: number | null;
  fighter_1_sig_strikes_att: number | null;
  fighter_1_sig_strikes_succ: number | null;
  fighter_1_takedown_att: number | null;
  fighter_1_takedown_succ: number | null;
  fighter_1_submission_att: number | null;
  fighter_1_reversals: number | null;
  fighter_1_ctrl_time: string | null;

  fighter_2_knockdowns: number | null;
  fighter_2_total_strikes_att: number | null;
  fighter_2_total_strikes_succ: number | null;
  fighter_2_sig_strikes_att: number | null;
  fighter_2_sig_strikes_succ: number | null;
  fighter_2_takedown_att: number | null;
  fighter_2_takedown_succ: number | null;
  fighter_2_submission_att: number | null;
  fighter_2_reversals: number | null;
  fighter_2_ctrl_time: string | null;
}

function FightDetails() {
  const { fight_url } = useParams<{ fight_url: string }>();

  const [fight, setFight] = useState<FightDetailsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchFightDetails() {
      if (!fight_url) {
        setError("Fight URL is missing.");
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError(null);

        const response = await fetch(
          `/fight-details/?fight_url=${encodeURIComponent(fight_url)}`
        );

        if (!response.ok) {
          throw new Error("Failed to fetch fight details.");
        }

        const data = await response.json();

        if (data.detail === "Fight not found") {
          throw new Error("Fight not found.");
        }

        setFight(data);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "An unexpected error occurred."
        );
      } finally {
        setLoading(false);
      }
    }

    fetchFightDetails();
  }, [fight_url]);

  if (loading) {
    return (
      <>
        <Navbar />
        <main>
          <p>Loading fight details...</p>
        </main>
      </>
    );
  }

  if (error || !fight) {
    return (
      <>
        <Navbar />
        <main>
          <p>{error ?? "Fight not found."}</p>
          <Link to="/">Back to fights</Link>
        </main>
      </>
    );
  }

  const fighter1Stats = [
    ["Knockdowns", fight.fighter_1_knockdowns],
    ["Total Strikes Attempted", fight.fighter_1_total_strikes_att],
    ["Total Strikes Successful", fight.fighter_1_total_strikes_succ],
    ["Significant Strikes Attempted", fight.fighter_1_sig_strikes_att],
    ["Significant Strikes Successful", fight.fighter_1_sig_strikes_succ],
    ["Takedowns Attempted", fight.fighter_1_takedown_att],
    ["Takedowns Successful", fight.fighter_1_takedown_succ],
    ["Submission Attempts", fight.fighter_1_submission_att],
    ["Reversals", fight.fighter_1_reversals],
    ["Control Time", fight.fighter_1_ctrl_time],
  ] as const;

  const fighter2Stats = [
    ["Knockdowns", fight.fighter_2_knockdowns],
    ["Total Strikes Attempted", fight.fighter_2_total_strikes_att],
    ["Total Strikes Successful", fight.fighter_2_total_strikes_succ],
    ["Significant Strikes Attempted", fight.fighter_2_sig_strikes_att],
    ["Significant Strikes Successful", fight.fighter_2_sig_strikes_succ],
    ["Takedowns Attempted", fight.fighter_2_takedown_att],
    ["Takedowns Successful", fight.fighter_2_takedown_succ],
    ["Submission Attempts", fight.fighter_2_submission_att],
    ["Reversals", fight.fighter_2_reversals],
    ["Control Time", fight.fighter_2_ctrl_time],
  ] as const;

  const formatValue = (value: string | number | boolean | null) => {
    if (value === null || value === undefined || value === "") {
      return "N/A";
    }

    if (typeof value === "boolean") {
      return value ? "Yes" : "No";
    }

    return String(value);
  };

  return (
    <>
      <Navbar />

      <main>
        <Link to="/">← Back to fights</Link>

        <section>
          <h1>
            {fight.fighter_1 ?? "Unknown Fighter"} vs.{" "}
            {fight.fighter_2 ?? "Unknown Fighter"}
          </h1>

          <p>{fight.event_name ?? "Event unavailable"}</p>

          <h2>Fight Details</h2>

          <dl>
            <dt>Weight Class</dt>
            <dd>{formatValue(fight.weight_class)}</dd>

            <dt>Gender</dt>
            <dd>{formatValue(fight.gender)}</dd>

            <dt>Title Fight</dt>
            <dd>{formatValue(fight.title_fight)}</dd>

            <dt>Scheduled Rounds</dt>
            <dd>{formatValue(fight.num_rounds)}</dd>

            <dt>Referee</dt>
            <dd>{formatValue(fight.referee)}</dd>

            <dt>Winner</dt>
            <dd>{formatValue(fight.winner)}</dd>

            <dt>Result</dt>
            <dd>{formatValue(fight.result)}</dd>

            <dt>Result Details</dt>
            <dd>{formatValue(fight.result_details)}</dd>

            <dt>Finish Round</dt>
            <dd>{formatValue(fight.finish_round)}</dd>

            <dt>Finish Time</dt>
            <dd>{formatValue(fight.finish_time)}</dd>
          </dl>
        </section>

        <section>
          <h2>Fight Statistics</h2>

          <div>
            <h3>{fight.fighter_1 ?? "Fighter 1"}</h3>

            <table>
              <thead>
                <tr>
                  <th>Statistic</th>
                  <th>Value</th>
                </tr>
              </thead>

              <tbody>
                {fighter1Stats.map(([label, value]) => (
                  <tr key={label}>
                    <td>{label}</td>
                    <td>{formatValue(value)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div>
            <h3>{fight.fighter_2 ?? "Fighter 2"}</h3>

            <table>
              <thead>
                <tr>
                  <th>Statistic</th>
                  <th>Value</th>
                </tr>
              </thead>

              <tbody>
                {fighter2Stats.map(([label, value]) => (
                  <tr key={label}>
                    <td>{label}</td>
                    <td>{formatValue(value)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </>
  );
}

export default FightDetails;

