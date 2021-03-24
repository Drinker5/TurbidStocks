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
  data() {
    return {
      loading: false,
    };
  },
  mounted() {
    this.loadGroupCandles();
  },
  watch: {
    dateRange() {
      this.loadGroupCandles();
    },
    interval() {
      this.loadGroupCandles();
    },
  },
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
    ...mapState(["groupCandles", "interval", "dateRange", "instrument"]),
  },
  methods: {
    loadGroupCandles() {
      if (!this.dateRange) return;
      this.loading = true;
      this.$stockService
        .loadGroupCandles({
          figi: this.instrument.figi,
          interval: this.$store.getters.intervalRequestParam,
          from: this.dateRange[0],
          to: this.dateRange[1],
        })
        .then((response) => {
          this.$store.commit("setGroupCandles", response.data.results);
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>

<style></style>
