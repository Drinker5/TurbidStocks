<template>
  <div>
    <Progress />
    <el-date-picker
      v-model="dateRange"
      type="daterange"
      align="right"
      unlink-panels
      range-separator="To"
      start-placeholder="Start date"
      end-placeholder="End date"
      :shortcuts="shortcuts"
    >
    </el-date-picker>
    <div v-if="instrument">
      <StockChart
        :instrument="instrument"
        :loading="loading"
        :candles="candles"
      />
    </div>
  </div>

  <div v-if="instrument">
    <Simulator :instrument="instrument" :candles="candles" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      loading: false,
      instrument: null,
      ticker: this.$route.params.id,
      dateRange: null,
      candles: null,
      intardayCandles: null,
      shortcuts: [
        {
          text: "Last week",
          value: (() => {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
            return [start, end];
          })(),
        },
        {
          text: "Last month",
          value: (() => {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
            return [start, end];
          })(),
        },
        {
          text: "Last 3 months",
          value: (() => {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
            return [start, end];
          })(),
        },
        {
          text: "Last year",
          value: (() => {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 365);
            return [start, end];
          })(),
        },
      ],
      intervalOptions: [
        { value: "1min", label: "1min", step: "00:01" },
        { value: "5min", label: "5min", step: "00:05" },
        { value: "10min", label: "10min", step: "00:10" },
        { value: "15min", label: "15min", step: "00:15" },
        { value: "30min", label: "30min", step: "00:30" },
      ],
    };
  },
  mounted() {
    let from = new Date();
    from.setFullYear(from.getFullYear() - 1);
    this.dateRange = [from, new Date()];

    this.loadInstrument();
  },
  watch: {
    dateRange() {
      if (!this.loading) this.loadDayCandles();
    },
  },
  computed: {},
  methods: {
    loadInstrument() {
      this.loading = true;
      this.$stockService
        .loadInstrument(this.ticker)
        .then((response) => {
          this.instrument = response.data;
          this.loadDayCandles();
        })
        .finally(() => {
          this.loading = false;
        });
    },
    loadDayCandles() {
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
