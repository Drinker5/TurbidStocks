import { createStore } from 'vuex'

// Create a new store instance.
const store = createStore({
  state() {
    return {
      instrument: null
    }
  },
  mutations: {
    setInstrument(state, instrument) {
      state.instrument = instrument
    }
  }
})

export default store;