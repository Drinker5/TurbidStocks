<template>
  <div v-loading="loading">
    <vue-highcharts
      type="chart"
      :options="chartOptions"
      :redrawOnUpdate="true"
      :oneToOneUpdate="false"
      :animateOnUpdate="true"
    />
  </div>
</template>

<script>
import VueHighcharts from "vue3-highcharts";
import { mapState } from "vuex";
export default {
  props: {},
  components: {
    VueHighcharts,
  },
  date() {
    return {
      loading: false,
    };
  },
  watch: {},
  computed: {
    chartOptions() {
      return {
        chart: {
          type: "line",
        },
        title: "",
        xAxis: {
          categories: this.groupCandles.map((i) => {
            return i.time__time;
          }),
        },
        yAxis: {
          title: {
            text: "",
          },
        },
        series: [
          {
            name: "Average open price",
            data: this.groupCandles.map((i) => {
              return i.o;
            }),
          },
        ],
      };
    },
    ...mapState(["groupCandles"]),
  },
  methods: {},
};
</script>

<style></style>
