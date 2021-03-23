<template>
  <Progress />
  <div v-if="instrument">
    <Simulator :candles="candles" :date-range="dateRange" />
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  data() {
    return {
      loading: false,
      ticker: this.$route.params.id,
      candles: null,
      intardayCandles: null,
    };
  },
  mounted() {
    this.loadInstrument();
  },
  watch: {
    dateRange() {
      if (!this.loading) this.loadDayCandles();
    },
  },
  computed: mapState(["instrument", "dateRange"]),
  methods: {
    loadInstrument() {
      this.loading = true;
      this.$stockService
        .loadInstrument(this.ticker)
        .then((response) => {
          this.$store.commit("setInstrument", response.data);
          this.loadDayCandles();
        })
        .finally(() => {
          this.loading = false;
        });
    },
    loadDayCandles() {
      if (!this.dateRange) return;
      this.$stockService
        .loadCandles({
          figi: this.instrument.figi,
          interval: "day",
          from: this.dateRange[0],
          to: this.dateRange[1],
        })
        .then((response) => {
          this.candles = response.data.results;
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>

<style></style>
