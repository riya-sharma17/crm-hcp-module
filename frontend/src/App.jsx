import { Routes, Route, Navigate } from 'react-router-dom'
import LogInteractionPage from './pages/LogInteraction/LogInteractionPage'

function App() {
  return (
    <div className="app">
      <Routes>
        <Route path="/" element={<Navigate to="/log-interaction" />} />
        <Route path="/log-interaction" element={<LogInteractionPage />} />
      </Routes>
    </div>
  )
}

export default App