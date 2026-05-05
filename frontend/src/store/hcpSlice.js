import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import api from '../services/api'

// Async action - search HCPs from backend
export const searchHCPs = createAsyncThunk(
  'hcp/search',
  async (query) => {
    const response = await api.get(`/api/hcp/search?name=${query}`)
    return response.data
  }
)

// Async action - get all HCPs
export const fetchAllHCPs = createAsyncThunk(
  'hcp/fetchAll',
  async () => {
    const response = await api.get('/api/hcp/')
    return response.data
  }
)

const hcpSlice = createSlice({
  name: 'hcp',
  initialState: {
    hcps: [],
    searchResults: [],
    selectedHCP: null,
    loading: false,
    error: null,
  },
  reducers: {
    // Synchronous actions
    setSelectedHCP: (state, action) => {
      state.selectedHCP = action.payload
    },
    clearSearchResults: (state) => {
      state.searchResults = []
    },
  },
  extraReducers: (builder) => {
    // Handle searchHCPs
    builder
      .addCase(searchHCPs.pending, (state) => {
        state.loading = true
      })
      .addCase(searchHCPs.fulfilled, (state, action) => {
        state.loading = false
        state.searchResults = action.payload
      })
      .addCase(searchHCPs.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message
      })
    // Handle fetchAllHCPs
    builder
      .addCase(fetchAllHCPs.fulfilled, (state, action) => {
        state.hcps = action.payload
      })
  },
})

export const { setSelectedHCP, clearSearchResults } = hcpSlice.actions
export default hcpSlice.reducer