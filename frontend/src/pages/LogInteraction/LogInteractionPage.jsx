import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { fetchInteractions } from '../../store/interactionSlice'
import { fetchAllHCPs } from '../../store/hcpSlice'
import InteractionForm from '../../components/form/InteractionForm'
import AIChat from '../../components/chat/AIChat'
import './LogInteractionPage.css'

function LogInteractionPage() {
  const dispatch = useDispatch()
  const { interactions } = useSelector((state) => state.interaction)

  useEffect(() => {
    dispatch(fetchInteractions())
    dispatch(fetchAllHCPs())
  }, [dispatch])

  return (
    <div className="page-wrapper">
      {/* Top Header */}
      <header className="page-header">
        <div className="header-left">
          <div className="header-logo">
            <span className="logo-icon">⚕</span>
            <span className="logo-text">PharmaCRM</span>
          </div>
          <div className="header-divider" />
          <h1 className="page-title">Log HCP Interaction</h1>
        </div>
        <div className="header-right">
          <div className="header-stat">
            <span className="stat-number">{interactions.length}</span>
            <span className="stat-label">Total Logs</span>
          </div>
          <div className="header-avatar">R</div>
        </div>
      </header>

      {/* Main Content */}
      <main className="page-content">
        {/* Left Panel - Form */}
        <div className="panel-left">
          <InteractionForm />
        </div>

        {/* Right Panel - AI Chat */}
        <div className="panel-right">
          <AIChat />
        </div>
      </main>
    </div>
  )
}

export default LogInteractionPage