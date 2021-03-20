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
  <div>Tax total: {{ taxTotal() }} {{ instrument.currency }}</div>
  <div>Performance: {{ performance() }}%</div>
</template>

<script>
import VueHighcharts from "vue3-highcharts";
import HighCharts from "highcharts";
import StockCharts from "highcharts/modules/stock";
import moment from "moment";
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
        title: {
          text: "Value",
        },
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
  methods: {
    taxTotal() {
      if (this.operations.length > 0)
        var x = this.operations.reduce((a, b) => {
          return { tax: a.tax + b.tax };
        }).tax;
      return Math.round(x * 100) / 100;
    },
    performance() {
      if (this.operations.length <= 0) return;

      let start = this.operations[0];
      let end = this.operations[this.operations.length - 1];
      let days = moment(end.time).diff(moment(start.time), "days");

      let startValue = start.value;
      let endValue = end.value;
      let result = (100 * (endValue / startValue - 1)) / (days / 365);
      return Math.round(result * 100) / 100;
    },
  },
};
</script>

<style></style>
