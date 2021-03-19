<template>
  <el-input placeholder="Start value" v-model="startValue" type="number">
    <template #suffix>
      {{
        instrument.currency == "USD"
          ? "$"
          : instrument.currency == "EUR"
          ? "€"
          : "₽"
      }}
    </template>
  </el-input>

  <el-input-number
    v-model="brokerTax"
    :precision="3"
    :step="0.05"
    :min="0"
    :max="100"
    placeholder="Broker tax"
  >
  </el-input-number>

  <el-slider
    v-model="buySellTimes"
    range
    show-stops
    :format-tooltip="formatTooltip"
    :min="minTime"
    :max="maxTime"
    :step="step"
    show-input
  >
  </el-slider>
</template>

<script>
export default {
  props: {
    instrument: Object,
    candles: Array,
  },
  components: {},

  data() {
    return {
      opretions: [],
      value: 0,
      brokerTax: 0.05,
      startValue: 1000,
      buySellTimes: [(7 * 60 + 30) * 60 * 1000, 18 * 60 * 60 * 1000],
      minTime: 7 * 60 * 60 * 1000,
      maxTime: 23 * 60 * 60 * 1000,
      step: 15 * 60 * 1000,
    };
  },
  mounted() {},
  watch: {
    candles(newV) {
      this.loadIntradayCandles(newV[0]);
    },
  },
  computed: {},
  methods: {
    loadIntradayCandles(candle) {
      let from = new Date(candle.time);
      let to = new Date(from);
      to.setDate(to.getDate() + 1);

      this.loading = true;
      this.$stockService
        .loadCandles({
          figi: this.instrument.figi,
          interval: "15min",
          from: from,
          to: to,
          format: "json",
        })
        .then((response) => {
          this.intardayCandles = response.data.results;
          let startDate = new Date(this.intardayCandles[0].time);

          // добавим сдвиг чтобы попасть в UTC
          let base = startDate.setHours(
            0,
            -startDate.getTimezoneOffset(),
            0,
            0
          );

          let l = new Date(this.intardayCandles[0].time).getTime();
          let r = new Date(
            this.intardayCandles[this.intardayCandles.length - 1].time
          ).getTime();

          this.minTime = l - base;
          this.maxTime = r - base;
          this.step = 15 * 60 * 1000; // 15 минутный шаг
        })
        .finally(() => {
          this.loading = false;
        });
    },

    formatTooltip(val) {
      let d = new Date(val);
      return `${d.getHours()}:${d
        .getMinutes()
        .toString()
        .padStart(2, "0")}`;
    },
  },
};
</script>

<style scoped></style>
