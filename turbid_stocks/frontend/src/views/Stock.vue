<template>
  <Progress />
  <el-form label-width="120px" size="mini">
    <el-form-item label="Date range">
      <el-date-picker
        v-model="dateRange"
        type="daterange"
        unlink-panels
        range-separator="To"
        start-placeholder="Start date"
        end-placeholder="End date"
        :shortcuts="shortcuts"
        :default-time="defaultTime"
        :disabled-date="disabledDate"
        format="DD.MM.YYYY"
      >
      </el-date-picker>
    </el-form-item>
  </el-form>

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
      dateRange: null,
      defaultTime: [
        new Date(2000, 1, 1, 0, 0, 0),
        new Date(2000, 2, 1, 0, 0, 0),
      ],
      candles: null,
      intardayCandles: null,
      shortcuts: [
        {
          text: "1 Month",
          value: (() => {
            let x = new Date();
            return [
              new Date(x.getFullYear(), x.getMonth() - 1, x.getDate()),
              new Date(x.getFullYear(), x.getMonth(), x.getDate()),
            ];
          })(),
        },
        {
          text: "3 Months",
          value: (() => {
            let x = new Date();
            return [
              new Date(x.getFullYear(), x.getMonth() - 3, x.getDate()),
              new Date(x.getFullYear(), x.getMonth(), x.getDate()),
            ];
          })(),
        },
        {
          text: "1 Year",
          value: (() => {
            let x = new Date();
            return [
              new Date(x.getFullYear() - 1, x.getMonth(), x.getDate()),
              new Date(x.getFullYear(), x.getMonth(), x.getDate()),
            ];
          })(),
        },
        {
          text: "2 Years",
          value: (() => {
            let x = new Date();
            return [
              new Date(x.getFullYear() - 2, x.getMonth(), x.getDate()),
              new Date(x.getFullYear(), x.getMonth(), x.getDate()),
            ];
          })(),
        },
        {
          text: "3 Years",
          value: (() => {
            let x = new Date();
            return [
              new Date(x.getFullYear() - 3, x.getMonth(), x.getDate()),
              new Date(x.getFullYear(), x.getMonth(), x.getDate()),
            ];
          })(),
        },
        {
          text: "5 Years",
          value: (() => {
            let x = new Date();
            return [
              new Date(x.getFullYear() - 5, x.getMonth(), x.getDate()),
              new Date(x.getFullYear(), x.getMonth(), x.getDate()),
            ];
          })(),
        },
      ],
      disabledDate(time) {
        return time.getTime() > Date.now();
      },
    };
  },
  mounted() {
    let x = new Date();
    this.dateRange = [
      new Date(x.getFullYear() - 1, x.getMonth(), x.getDate()),
      new Date(x.getFullYear(), x.getMonth(), x.getDate()),
    ];

    this.loadInstrument();
  },
  watch: {
    dateRange() {
      if (!this.loading) this.loadDayCandles();
    },
  },
  computed: mapState(["instrument"]),
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
