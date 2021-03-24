import { createStore } from 'vuex'

// Create a new store instance.
const store = createStore({
  state() {
    return {
      instrument: null,
      groupCandles: [],
      dateRange: null,
      interval: 15,
      dayCandles: null
    }
  },
  getters: {
    intervalRequestParam(state) {
      return state.interval < 60 ? `${state.interval}min` : "hour";
    },
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
    },
    setInterval(state, interval) {
      state.interval = interval
    },
    setDayCandles(state, dayCandles) {
      state.dayCandles = dayCandles
    }
  }
})

export default store;