import { createStore } from 'vuex'

// Create a new store instance.
const store = createStore({
  state() {
    return {
      instrument: null,
      groupCandles: [],
      dateRange: null
    }
  },
  mutations: {
    setInstrument(state, instrument) {
      state.instrument = instrument
    },
    setGroupCandles(state, candles) {
      state.groupCandles = candles
    },
    setDateRange(state, dateRange) {
      state.dateRange = dateRange
    }
  }
})

export default store;