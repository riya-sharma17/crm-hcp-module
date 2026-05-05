import { configureStore } from '@reduxjs/toolkit'
import hcpReducer from './hcpSlice'
import interactionReducer from './interactionSlice'

const store = configureStore({
  reducer: {
    hcp: hcpReducer,
    interaction: interactionReducer,
  },
})

export default store