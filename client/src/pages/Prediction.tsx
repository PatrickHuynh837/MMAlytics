import { useState } from "react";
import Navbar from "../components/Navbar";

function Prediction() {
const [activeTab, setActiveTab] = useState<"past" | "upcoming">("past");

return ( <div> <Navbar />

  <h1>Prediction</h1>

  <div>
    <button
      onClick={() => setActiveTab("past")}
      className={activeTab === "past" ? "active" : ""}
    >
      Past Results
    </button>

    <button
      onClick={() => setActiveTab("upcoming")}
      className={activeTab === "upcoming" ? "active" : ""}
    >
      Upcoming Fights
    </button>
  </div>

  <div>
    {activeTab === "past" && (
      <div>
        <h2>Past Results</h2>
        {/* Display historical fight results here */}
      </div>
    )}

    {activeTab === "upcoming" && (
      <div>
        <h2>Upcoming Fights</h2>
        {/* Display upcoming fights and predictions here */}
      </div>
    )}
  </div>
</div>


);
}

export default Prediction;
