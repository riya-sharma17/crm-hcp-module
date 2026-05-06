import { useState, useRef, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { FiSend, FiUser, FiCpu } from 'react-icons/fi'
import { sendChatMessage, addChatMessage } from '../../store/interactionSlice'
import Button from '../common/Button'
import './AIChat.css'

const SUGGESTIONS = [
  'Met Dr. Smith, discussed Product X efficacy',
  'Called Dr. Patel about new guidelines',
  'Shared brochure with Dr. Kumar',
]

function AIChat() {
  const dispatch = useDispatch()
  const { chatMessages, chatLoading } = useSelector(
    (state) => state.interaction
  )
  const [input, setInput] = useState('')
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [chatMessages])

  const handleSend = () => {
    if (!input.trim() || chatLoading) return

    // Add user message to chat
    dispatch(addChatMessage({
      role: 'user',
      content: input,
    }))

    // Send to agent
    dispatch(sendChatMessage(input))
    setInput('')
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleSuggestion = (suggestion) => {
    setInput(suggestion)
  }

  return (
    <div className="chat-panel">
      {/* Header */}
      <div className="chat-header">
        <div className="chat-header-left">
          <div className="chat-avatar">
            <FiCpu />
          </div>
          <div>
            <h3 className="chat-title">AI Assistant</h3>
            <span className="chat-subtitle">Log interaction via chat</span>
          </div>
        </div>
        <div className="chat-status">
          <span className="status-dot" />
          <span>Online</span>
        </div>
      </div>

      {/* Messages */}
      <div className="chat-messages">
        {chatMessages.length === 0 ? (
          <div className="chat-empty">
            <div className="chat-empty-icon">
              <FiCpu />
            </div>
            <p className="chat-empty-title">
              Log interaction details here
            </p>
            <p className="chat-empty-subtitle">
              Describe your interaction naturally and I'll extract
              the key details automatically.
            </p>

            {/* Suggestions */}
            <div className="chat-suggestions">
              {SUGGESTIONS.map((s, i) => (
                <button
                  key={i}
                  className="chat-suggestion"
                  onClick={() => handleSuggestion(s)}
                >
                  "{s}"
                </button>
              ))}
            </div>
          </div>
        ) : (
          chatMessages.map((msg, i) => (
            <div
              key={i}
              className={`chat-message ${msg.role === 'user' ? 'user' : 'assistant'}`}
            >
              <div className="message-avatar">
                {msg.role === 'user' ? <FiUser /> : <FiCpu />}
              </div>
              <div className="message-content">
                <div className="message-bubble">
                  {msg.content}
                </div>
                {msg.interaction && (
                  <div className="message-logged">
                    ✅ Interaction logged successfully
                  </div>
                )}
              </div>
            </div>
          ))
        )}

        {/* Loading indicator */}
        {chatLoading && (
          <div className="chat-message assistant">
            <div className="message-avatar">
              <FiCpu />
            </div>
            <div className="message-content">
              <div className="message-bubble typing">
                <span /><span /><span />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="chat-input-area">
        <textarea
          className="chat-input"
          placeholder="Describe interaction..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={2}
        />
        <Button
          variant="primary"
          size="md"
          onClick={handleSend}
          loading={chatLoading}
          disabled={!input.trim()}
          icon={<FiSend />}
        >
          Log
        </Button>
      </div>
    </div>
  )
}

export default AIChat