
import axios from "axios";
import qs from 'qs'

export default {
  install: (app) => {
    app.config.globalProperties.$stockService = {
      loadCandles: ({ figi, interval, from, to, hours, minutes }) => {
        return axios
          .get("/api/candles/", {
            params: {
              figi: figi,
              interval: interval,
              from: from,
              to: to,
              format: "json",
              hours: hours,
              minutes: minutes
            },
            paramsSerializer: params => {
              return qs.stringify(params, { arrayFormat: "repeat" })
            }
          })
      },

      loadGroupCandles: ({ figi, interval, from, to }) => {
        return axios
          .get("/api/candles/group_candles/", {
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