import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import api from '../services/api'

export const createInteraction = createAsyncThunk(
  'interaction/create',
  async (interactionData) => {
    const response = await api.post('/api/interactions/', interactionData)
    return response.data
  }
)

export const fetchInteractions = createAsyncThunk(
  'interaction/fetchAll',
  async (hcpId = null) => {
    const url = hcpId
      ? `/api/interactions/?hcp_id=${hcpId}`
      : '/api/interactions/'
    const response = await api.get(url)
    return response.data
  }
)

export const updateInteraction = createAsyncThunk(
  'interaction/update',
  async ({ id, data }) => {
    const response = await api.put(`/api/interactions/${id}`, data)
    return response.data
  }
)

export const sendChatMessage = createAsyncThunk(
  'interaction/chat',
  async (message) => {
    const response = await api.post('/api/agent/chat', { message })
    return response.data
  }
)

const interactionSlice = createSlice({
  name: 'interaction',
  initialState: {
    interactions: [],
    currentInteraction: null,
    chatMessages: [],
    chatLoading: false,
    formLoading: false,
    successMessage: null,
    error: null,
    // NEW - extracted form data from chat
    extractedFormData: null,
  },
  reducers: {
    addChatMessage: (state, action) => {
      state.chatMessages.push(action.payload)
    },
    clearSuccess: (state) => {
      state.successMessage = null
    },
    clearError: (state) => {
      state.error = null
    },
    resetForm: (state) => {
      state.currentInteraction = null
      state.successMessage = null
      state.error = null
      state.extractedFormData = null
    },
    // NEW - manually set extracted data
    setExtractedFormData: (state, action) => {
      state.extractedFormData = action.payload
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(createInteraction.pending, (state) => {
        state.formLoading = true
        state.error = null
      })
      .addCase(createInteraction.fulfilled, (state, action) => {
        state.formLoading = false
        state.interactions.unshift(action.payload)
        state.successMessage = 'Interaction logged successfully!'
        state.currentInteraction = action.payload
      })
      .addCase(createInteraction.rejected, (state, action) => {
        state.formLoading = false
        state.error = action.error.message
      })

    builder
      .addCase(fetchInteractions.fulfilled, (state, action) => {
        state.interactions = action.payload
      })

    builder
      .addCase(updateInteraction.fulfilled, (state, action) => {
        const index = state.interactions.findIndex(
          (i) => i.id === action.payload.id
        )
        if (index !== -1) {
          state.interactions[index] = action.payload
        }
        state.successMessage = 'Interaction updated successfully!'
      })

    builder
      .addCase(sendChatMessage.pending, (state) => {
        state.chatLoading = true
      })
      .addCase(sendChatMessage.fulfilled, (state, action) => {
        state.chatLoading = false

        // Add AI response to chat
        state.chatMessages.push({
          role: 'assistant',
          content: action.payload.message,
          interaction: action.payload.interaction,
        })

        // AUTO FILL FORM
        const extracted = action.payload.extracted_form_data
        console.log('Extracted form data:', extracted)

        if (extracted && Object.keys(extracted).length > 0) {
          state.extractedFormData = extracted
          console.log('Form data set in Redux:', state.extractedFormData)
        }

        if (action.payload.interaction) {
          state.interactions.unshift(action.payload.interaction)
          state.successMessage = 'Interaction logged via chat!'
        }
      })
      .addCase(sendChatMessage.rejected, (state, action) => {
        state.chatLoading = false
        state.error = action.error.message
      })
  },
})

export const {
  addChatMessage,
  clearSuccess,
  clearError,
  resetForm,
  setExtractedFormData
} = interactionSlice.actions

export default interactionSlice.reducer