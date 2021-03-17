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
    <el-select v-model="interval" placeholder="Interval">
      <el-option
        v-for="item in intervalOptions"
        :key="item.value"
        :label="item.label"
        :value="item.value"
        :disabled="item.disabled"
      >
      </el-option>
    </el-select>
    <div v-if="instrument">
      <StockChart
        :instrument="instrument"
        :from="dateRange ? dateRange[0] : null"
        :to="dateRange ? dateRange[1] : null"
        :interval="interval"
      />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loading: false,
      instrument: null,
      ticker: this.$route.params.id,
      dateRange: "",
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
        { value: "1min", label: "1min" },
        { value: "2min", label: "2min", disabled: true },
        { value: "3min", label: "3min", disabled: true },
        { value: "5min", label: "5min" },
        { value: "10min", label: "10min", disabled: true },
        { value: "15min", label: "15min" },
        { value: "30min", label: "30min", disabled: true },
        { value: "hour", label: "hour" },
        { value: "day", label: "day" },
        { value: "week", label: "week" },
        { value: "month", label: "month" },
      ],
      interval: "day",
    };
  },
  mounted() {
    let from = new Date();
    from.setFullYear(from.getFullYear() - 1);
    this.dateRange = [from, new Date()];

    this.loadInstrument(this.ticker);
  },

  methods: {
    loadInstrument(ticker) {
      this.loading = true;
      this.axios
        .get(`/api/instruments/${ticker}/`, {
          params: {
            format: "json",
          },
        })
        .then((response) => {
          this.instrument = response.data;
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>

<style></style>
