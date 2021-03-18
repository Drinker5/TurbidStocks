<template>
  <div v-loading="loading">
    <vue-highcharts
      type="stockChart"
      :options="chartOptions"
      :redrawOnUpdate="false"
      :oneToOneUpdate="false"
      :animateOnUpdate="true"
      ref="chart"
    />
  </div>
</template>

<script>
import HighCharts from "highcharts";
import StockCharts from "highcharts/modules/stock";
import VueHighcharts from "vue3-highcharts";
StockCharts(HighCharts);
export default {
  props: {
    instrument: Object,
    from: Date,
    to: Date,
    interval: {
      type: String,
      default: "day",
    },
  },
  components: {
    VueHighcharts,
  },

  data() {
    return {
      candles: null,
      loading: false,
    };
  },
  mounted() {
    this.loadCandles();
  },
  watch: {
    interval() {
      this.loadCandles();
    },
    from(newV) {
      if (!this.loading && newV) this.loadCandles();
    },
    to(newV) {
      if (!this.loading && newV) this.loadCandles();
    },
  },
  computed: {
    chartOptions() {
      return {
        title: {
          text: this.instrument.name,
        },
        series: [
          {
            type: "candlestick",
            name: this.instrument.ticker,
            data: this.candles,
          },
        ],
      };
    },
  },
  methods: {
    loadCandles() {
      this.loading = true;
      this.axios
        .get("/api/candles/", {
          params: {
            figi: this.instrument.figi,
            interval: this.interval,
            from: this.from,
            to: this.to,
            format: "json",
          },
        })
        .then((response) => {
          this.candles = response.data.results.map((i) => {
            //[new Date(i.time), i.o, i.h, i.l, i.c];
            return [new Date(i.time).getTime(), i.o, i.h, i.l, i.c];
          });

          setTimeout(() => {
            this.$refs.chart.chart.redraw();
          }, 0);
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
