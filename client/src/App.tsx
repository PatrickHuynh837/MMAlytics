import './App.css'
import Home from './pages/Home'
import Analytics from './pages/Analytics'
import Comparison from './pages/Comparison'
import Dashboard from './pages/Dashboard'
import Events from './pages/Events'
import FighterProfile from './pages/FighterProfile'
import Matchup from './pages/Matchup'
import Prediction from './pages/Prediction'
import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/comparison" element={<Comparison />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/events" element={<Events />} />
        <Route path="/fighters" element={<FighterProfile />} />
        <Route path="/matchup" element={<Matchup />} />
        <Route path="/prediction" element={<Prediction />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
