
import axios from "axios";

export default {
  install: (app) => {
    app.config.globalProperties.$stockService = {
      loadCandles: ({ figi, interval, from, to }) => {
        return axios
          .get("/api/candles/", {
            params: {
              figi: figi,
              interval: interval,
              from: from,
              to: to,
              format: "json",
            },
          })
      },

      loadInstrument: (ticker) => {
        return axios
          .get(`/api/instruments/${ticker}/`, {
            params: {
              format: "json",
            },
          })
      },
    }
  }
}