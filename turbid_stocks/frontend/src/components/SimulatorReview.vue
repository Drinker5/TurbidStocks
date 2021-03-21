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
import VueHighcharts from "vue3-highcharts";
import HighCharts from "highcharts";
import StockCharts from "highcharts/modules/stock";
StockCharts(HighCharts);
export default {
  props: {
    instrument: Object,
    loading: Boolean,
    operations: Array,
  },
  components: {
    VueHighcharts,
  },
  watch: {},
  computed: {
    chartOptions() {
      return {
        time: {
          useUTC: false,
        },
        series: [
          {
            name: this.instrument.currency,
            data: this.operations.map((i) => {
              let time = i.time.getTime();
              return [time, i.value];
            }),
          },
        ],
      };
    },
  },
  methods: {},
};
</script>

<style></style>
