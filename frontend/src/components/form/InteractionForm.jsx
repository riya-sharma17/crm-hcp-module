import { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { FiCalendar, FiClock, FiUsers } from 'react-icons/fi'
import { createInteraction } from '../../store/interactionSlice'
import { searchHCPs, setSelectedHCP } from '../../store/hcpSlice'
import Input from '../common/Input'
import Select from '../common/Select'
import Button from '../common/Button'
import HCPSearchDropdown from './HCPSearchDropdown'
import SentimentSelector from './SentimentSelector'
import MaterialsSection from './MaterialsSection'
import FollowUpSection from './FollowUpSection'
import './InteractionForm.css'

const INTERACTION_TYPES = [
  { value: 'Meeting', label: 'Meeting' },
  { value: 'Call', label: 'Call' },
  { value: 'Email', label: 'Email' },
  { value: 'Conference', label: 'Conference' },
  { value: 'Virtual', label: 'Virtual' },
]

function InteractionForm() {
  const dispatch = useDispatch()

  // Step 1 - all useSelector hooks first
  const { selectedHCP } = useSelector((state) => state.hcp)
  const { formLoading, successMessage, error, extractedFormData } = useSelector(
    (state) => state.interaction
  )

  // Step 2 - all useState hooks
  const [form, setForm] = useState({
    interaction_type: 'Meeting',
    interaction_date: new Date().toISOString().split('T')[0],
    interaction_time: new Date().toTimeString().slice(0, 5),
    attendees: '',
    topics_discussed: '',
    sentiment: 'Neutral',
    outcomes: '',
    follow_up_actions: [],
    materials_shared: [],
    samples_distributed: [],
  })

 useEffect(() => {
  console.log('extractedFormData changed:', extractedFormData)
  if (!extractedFormData) return

  console.log('Filling form with:', extractedFormData)

  setForm((prev) => ({
    ...prev,
    interaction_type:
      extractedFormData.interaction_type || prev.interaction_type,
    topics_discussed:
      extractedFormData.topics_discussed || prev.topics_discussed,
    sentiment: extractedFormData.sentiment || prev.sentiment,
    outcomes: extractedFormData.outcomes || prev.outcomes,
    follow_up_actions:
      extractedFormData.follow_up_actions?.length
        ? extractedFormData.follow_up_actions
        : prev.follow_up_actions,
    materials_shared:
      extractedFormData.materials_shared?.length
        ? extractedFormData.materials_shared
        : prev.materials_shared,
    samples_distributed:
      extractedFormData.samples_distributed?.length
        ? extractedFormData.samples_distributed
        : prev.samples_distributed,
    attendees:
      extractedFormData.attendees?.length
        ? extractedFormData.attendees.join(', ')
        : prev.attendees,
  }))

  if (extractedFormData.hcp_name) {
    console.log('Searching HCP:', extractedFormData.hcp_name)
    dispatch(searchHCPs(extractedFormData.hcp_name))
  }
}, [extractedFormData])

  const handleChange = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }))
  }

  const handleSubmit = () => {
    if (!selectedHCP) {
      alert('Please select an HCP first')
      return
    }

    const interactionDateTime = new Date(
      `${form.interaction_date}T${form.interaction_time}`
    ).toISOString()

    dispatch(
      createInteraction({
        hcp_id: selectedHCP.id,
        hcp_name: selectedHCP.name,
        interaction_type: form.interaction_type,
        interaction_date: interactionDateTime,
        attendees: form.attendees
          ? form.attendees.split(',').map((a) => a.trim())
          : [],
        topics_discussed: form.topics_discussed,
        sentiment: form.sentiment,
        outcomes: form.outcomes,
        follow_up_actions: form.follow_up_actions,
        materials_shared: form.materials_shared,
        samples_distributed: form.samples_distributed,
        logged_via: 'form',
      })
    )
  }

  return (
    <div className="form-panel">
      <div className="form-header">
        <h2 className="form-title">Interaction Details</h2>
      </div>

      <div className="form-body">
        {/* Row 1 - HCP Name + Interaction Type */}
        <div className="form-row">
          <div className="form-col">
            <label className="field-label">
              HCP Name <span className="required">*</span>
            </label>
            <HCPSearchDropdown />
          </div>
          <div className="form-col">
            <Select
              label="Interaction Type"
              value={form.interaction_type}
              onChange={(e) =>
                handleChange('interaction_type', e.target.value)
              }
              options={INTERACTION_TYPES}
            />
          </div>
        </div>

        {/* Row 2 - Date + Time */}
        <div className="form-row">
          <div className="form-col">
            <Input
              label="Date"
              type="date"
              value={form.interaction_date}
              onChange={(e) =>
                handleChange('interaction_date', e.target.value)
              }
              icon={<FiCalendar />}
            />
          </div>
          <div className="form-col">
            <Input
              label="Time"
              type="time"
              value={form.interaction_time}
              onChange={(e) =>
                handleChange('interaction_time', e.target.value)
              }
              icon={<FiClock />}
            />
          </div>
        </div>

        {/* Attendees */}
        <Input
          label="Attendees"
          placeholder="Enter names or search..."
          value={form.attendees}
          onChange={(e) => handleChange('attendees', e.target.value)}
          icon={<FiUsers />}
        />

        {/* Topics Discussed */}
        <div className="form-group">
          <label className="field-label">Topics Discussed</label>
          <textarea
            className="textarea-field"
            placeholder="Enter key discussion points..."
            value={form.topics_discussed}
            onChange={(e) =>
              handleChange('topics_discussed', e.target.value)
            }
            rows={3}
          />
        </div>

        {/* Materials Section */}
        <MaterialsSection
          materials={form.materials_shared}
          samples={form.samples_distributed}
          onMaterialsChange={(val) =>
            handleChange('materials_shared', val)
          }
          onSamplesChange={(val) =>
            handleChange('samples_distributed', val)
          }
        />

        {/* Sentiment */}
        <SentimentSelector
          value={form.sentiment}
          onChange={(val) => handleChange('sentiment', val)}
        />

        {/* Outcomes */}
        <div className="form-group">
          <label className="field-label">Outcomes</label>
          <textarea
            className="textarea-field"
            placeholder="Key outcomes or agreements..."
            value={form.outcomes}
            onChange={(e) => handleChange('outcomes', e.target.value)}
            rows={2}
          />
        </div>

        {/* Follow Up */}
        <FollowUpSection
          followUps={form.follow_up_actions}
          onChange={(val) => handleChange('follow_up_actions', val)}
        />

        {/* AI Fill Indicator */}
        {extractedFormData && (
          <div className="alert alert-info">
            ✨ Form auto-filled from AI chat
          </div>
        )}

        {/* Status Messages */}
        {successMessage && (
          <div className="alert alert-success">{successMessage}</div>
        )}
        {error && (
          <div className="alert alert-error">{error}</div>
        )}

        {/* Submit */}
        <Button
          variant="primary"
          size="lg"
          onClick={handleSubmit}
          loading={formLoading}
        >
          Log Interaction
        </Button>
      </div>
    </div>
  )
}

export default InteractionForm