import { useState } from 'react'
import { FiPlus, FiX } from 'react-icons/fi'
import './FollowUpSection.css'

function FollowUpSection({ followUps, onChange }) {
  const [input, setInput] = useState('')

  const addFollowUp = () => {
    if (input.trim()) {
      onChange([...followUps, input.trim()])
      setInput('')
    }
  }

  const removeFollowUp = (index) => {
    onChange(followUps.filter((_, i) => i !== index))
  }

  return (
    <div className="followup-section">
      <label className="field-label">Follow-up Actions</label>
      <textarea
        className="textarea-field"
        placeholder="Enter next steps or tasks..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        rows={2}
      />
      <button
        className="followup-add-btn"
        onClick={addFollowUp}
        type="button"
      >
        <FiPlus /> Add Follow-up
      </button>
      {followUps.length > 0 && (
        <div className="followup-list">
          {followUps.map((f, i) => (
            <div key={i} className="followup-item">
              <span className="followup-bullet">→</span>
              <span className="followup-text">{f}</span>
              <FiX
                className="followup-remove"
                onClick={() => removeFollowUp(i)}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default FollowUpSection