import { useState } from 'react'
import { FiPlus, FiX, FiSearch } from 'react-icons/fi'
import './MaterialsSection.css'

function MaterialsSection({
  materials,
  samples,
  onMaterialsChange,
  onSamplesChange,
}) {
  const [materialInput, setMaterialInput] = useState('')
  const [sampleInput, setSampleInput] = useState('')

  const addMaterial = () => {
    if (materialInput.trim()) {
      onMaterialsChange([
        ...materials,
        { name: materialInput.trim() },
      ])
      setMaterialInput('')
    }
  }

  const removeMaterial = (index) => {
    onMaterialsChange(materials.filter((_, i) => i !== index))
  }

  const addSample = () => {
    if (sampleInput.trim()) {
      onSamplesChange([
        ...samples,
        { name: sampleInput.trim() },
      ])
      setSampleInput('')
    }
  }

  const removeSample = (index) => {
    onSamplesChange(samples.filter((_, i) => i !== index))
  }

  return (
    <div className="materials-section">
      <label className="field-label">
        Materials Shared / Samples Distributed
      </label>

      {/* Materials */}
      <div className="materials-group">
        <div className="materials-header">
          <span className="materials-subtitle">Materials Shared</span>
          <div className="materials-input-row">
            <input
              type="text"
              className="materials-input"
              placeholder="Add material..."
              value={materialInput}
              onChange={(e) => setMaterialInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && addMaterial()}
            />
            <button
              className="materials-add-btn"
              onClick={addMaterial}
              type="button"
            >
              <FiSearch /> Search/Add
            </button>
          </div>
          <div className="materials-tags">
            {materials.length === 0 ? (
              <span className="materials-empty">No materials added</span>
            ) : (
              materials.map((m, i) => (
                <span key={i} className="material-tag">
                  {m.name}
                  <FiX onClick={() => removeMaterial(i)} />
                </span>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Samples */}
      <div className="materials-group">
        <div className="materials-header">
          <span className="materials-subtitle">Samples Distributed</span>
          <div className="materials-input-row">
            <input
              type="text"
              className="materials-input"
              placeholder="Add sample..."
              value={sampleInput}
              onChange={(e) => setSampleInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && addSample()}
            />
            <button
              className="materials-add-btn"
              onClick={addSample}
              type="button"
            >
              <FiPlus /> Add Sample
            </button>
          </div>
          <div className="materials-tags">
            {samples.length === 0 ? (
              <span className="materials-empty">No samples added</span>
            ) : (
              samples.map((s, i) => (
                <span key={i} className="material-tag sample">
                  {s.name}
                  <FiX onClick={() => removeSample(i)} />
                </span>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default MaterialsSection