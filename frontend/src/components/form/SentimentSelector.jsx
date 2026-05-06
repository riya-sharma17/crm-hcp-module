import './SentimentSelector.css'

const SENTIMENTS = [
  { value: 'Positive', emoji: '😊', color: 'positive' },
  { value: 'Neutral', emoji: '😐', color: 'neutral' },
  { value: 'Negative', emoji: '😞', color: 'negative' },
]

function SentimentSelector({ value, onChange }) {
  return (
    <div className="sentiment-wrapper">
      <label className="field-label">
        Observed/Inferred HCP Sentiment
      </label>
      <div className="sentiment-options">
        {SENTIMENTS.map((s) => (
          <label key={s.value} className="sentiment-option">
            <input
              type="radio"
              name="sentiment"
              value={s.value}
              checked={value === s.value}
              onChange={() => onChange(s.value)}
            />
            <span className={`sentiment-label ${s.color} ${value === s.value ? 'active' : ''}`}>
              {s.emoji} {s.value}
            </span>
          </label>
        ))}
      </div>
    </div>
  )
}

export default SentimentSelector