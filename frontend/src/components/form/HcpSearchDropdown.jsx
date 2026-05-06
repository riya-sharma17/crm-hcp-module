import { useState, useEffect, useRef } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { FiSearch, FiUser } from 'react-icons/fi'
import { searchHCPs, setSelectedHCP } from '../../store/hcpSlice'
import './HCPSearchDropdown.css'

function HCPSearchDropdown() {
  const dispatch = useDispatch()
  const { searchResults, selectedHCP, loading } = useSelector(
    (state) => state.hcp
  )
  const [query, setQuery] = useState('')
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef(null)

  useEffect(() => {
    if (query.length >= 2) {
      dispatch(searchHCPs(query))
      setIsOpen(true)
    } else {
      setIsOpen(false)
    }
  }, [query])

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setIsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleSelect = (hcp) => {
    dispatch(setSelectedHCP(hcp))
    setQuery(hcp.name)
    setIsOpen(false)
  }

  return (
    <div className="hcp-dropdown" ref={dropdownRef}>
      <div className="hcp-input-container">
        <FiSearch className="hcp-search-icon" />
        <input
          type="text"
          className="hcp-input"
          placeholder="Search or select HCP..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </div>

      {isOpen && (
        <div className="hcp-results">
          {loading ? (
            <div className="hcp-loading">Searching...</div>
          ) : searchResults.length > 0 ? (
            searchResults.map((hcp) => (
              <div
                key={hcp.id}
                className="hcp-result-item"
                onClick={() => handleSelect(hcp)}
              >
                <div className="hcp-result-icon">
                  <FiUser />
                </div>
                <div className="hcp-result-info">
                  <span className="hcp-result-name">{hcp.name}</span>
                  <span className="hcp-result-meta">
                    {hcp.specialty} {hcp.hospital && `· ${hcp.hospital}`}
                  </span>
                </div>
              </div>
            ))
          ) : (
            <div className="hcp-no-results">No HCPs found</div>
          )}
        </div>
      )}

      {selectedHCP && (
        <div className="hcp-selected-badge">
          <FiUser />
          <span>{selectedHCP.name}</span>
          {selectedHCP.specialty && (
            <span className="hcp-badge-meta">· {selectedHCP.specialty}</span>
          )}
        </div>
      )}
    </div>
  )
}

export default HCPSearchDropdown