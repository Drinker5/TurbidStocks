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
StockCharts(HighCharts);
export default {
  props: {
    instrument: Object,
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
    let from = new Date();
    from.setFullYear(from.getFullYear() - 1);
    this.loadCandles(from, new Date());
  },
  computed: {
    chartOptions() {
      return {
        rangeSelector: {
          selected: 5,
        },

        title: {
          text: this.instrument.name,
        },
        series: [
          {
            name: this.instrument.ticker,
            data: this.candles,
          },
        ],
      };
    },
  },
  methods: {
    loadCandles(from, to) {
      this.loading = true;
      this.axios
        .get("/api/candles/", {
          params: {
            figi: this.instrument.figi,
            interval: "day",
            from: from,
            to: to,
            format: "json",
          },
        })
        .then((response) => {
          this.candles = response.data.results.map((i) => {
            //[new Date(i.time), i.o, i.h, i.l, i.c];
            return [new Date(i.time).getTime(), i.c];
          });
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
