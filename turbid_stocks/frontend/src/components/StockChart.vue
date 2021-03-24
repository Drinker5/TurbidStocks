<template>
  <div v-loading="loading">
    <vue-highcharts
      type="stockChart"
      :options="chartOptions"
      :redrawOnUpdate="true"
      :oneToOneUpdate="false"
      :animateOnUpdate="true"
    />
  </div>
</template>

<script>
import HighCharts from "highcharts";
import StockCharts from "highcharts/modules/stock";
import VueHighcharts from "vue3-highcharts";
import { mapState } from "vuex";
StockCharts(HighCharts);
export default {
  props: {
    loading: Boolean,
  },
  components: {
    VueHighcharts,
  },

  data() {
    return {};
  },
  mounted() {},
  watch: {},
  computed: {
    chartOptions() {
      return {
        chart: {
          type: "candlestick",
          zoomType: "x",
        },

        time: {
          useUTC: false,
        },
        series: [
          {
            name: this.instrument.ticker,
            data: this.dayCandles
              ? this.dayCandles.map((i) => {
                  return [new Date(i.time).getTime(), i.o, i.h, i.l, i.c];
                })
              : null,
          },
        ],

        rangeSelector: {
          buttons: [
            {
              type: "month",
              count: 1,
              text: "1m",
            },
            {
              type: "year",
              count: 1,
              text: "1y",
            },
            {
              type: "all",
              text: "All",
            },
          ],
        },
      };
    },
    ...mapState(["instrument", "dayCandles"]),
  },
  methods: {},
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
