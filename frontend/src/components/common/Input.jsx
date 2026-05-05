import './Input.css'

function Input({
  label,
  type = 'text',
  placeholder,
  value,
  onChange,
  required,
  icon,
  error,
}) {
  return (
    <div className="input-wrapper">
      {label && (
        <label className="input-label">
          {label}
          {required && <span className="required">*</span>}
        </label>
      )}
      <div className="input-container">
        {icon && <span className="input-icon">{icon}</span>}
        <input
          type={type}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          className={`input-field ${icon ? 'with-icon' : ''} ${error ? 'error' : ''}`}
        />
      </div>
      {error && <span className="input-error">{error}</span>}
    </div>
  )
}

export default Input