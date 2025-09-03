import { Routes, Route, Link } from 'react-router-dom'
import AvailabilityPage from './pages/AvailabilityPage'

export default function App() {
  return (
    <div>
      <nav>
        <Link to="/">Home</Link> | <Link to="/availability">Availability</Link>
      </nav>
      <Routes>
        <Route path="/availability" element={<AvailabilityPage />} />
        <Route path="/" element={<div>Welcome to Parking Reservation System</div>} />
      </Routes>
    </div>
  )
}
