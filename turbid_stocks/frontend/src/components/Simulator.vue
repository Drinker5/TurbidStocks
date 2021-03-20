<template>
  <el-input placeholder="Start money" v-model="startMoney" type="number">
    <template #suffix>
      {{ instrument.currency }}
    </template>
  </el-input>

  <el-input-number
    v-model="brokerTax"
    :precision="3"
    :step="0.05"
    :min="0"
    :max="5"
    placeholder="Broker tax"
  >
  </el-input-number>

  <span>Buy time {{ formatTooltip(buyTime) }}</span>
  <span>Sell time {{ formatTooltip(sellTime) }}</span>
  <el-slider
    v-model="buySellTimes"
    range
    show-stops
    :format-tooltip="formatTooltip"
    :min="minTime"
    :max="maxTime"
    :step="step"
  >
  </el-slider>
  <el-checkbox v-model="isBuySellReversed">Reverse buy/sell</el-checkbox>
  <el-button type="primary" :loading="loading" @click="simulate">
    Simulate
  </el-button>

  <SimulatorReview
    :operations="operations"
    :loading="loading"
    :instrument="instrument"
  />
</template>

<script>
export default {
  props: {
    instrument: Object,
    candles: Array,
    dateRange: Array,
    interval: {
      type: Number,
      default: 15,
    },
  },
  components: {},

  data() {
    return {
      loading: false,
      operations: [],
      money: 0,
      stockCount: 0,
      brokerTax: 0.05,
      startMoney: 1000.0,
      buySellTimes: [(7 * 60 + 30) * 60 * 1000, 18 * 60 * 60 * 1000],
      minTime: 7 * 60 * 60 * 1000,
      maxTime: 23 * 60 * 60 * 1000,
      step: this.interval * 60 * 1000,
      intervalRequestParam: `${this.interval}min`,
      isBuySellReversed: false,
    };
  },
  mounted() {},
  watch: {
    candles(newV) {
      this.loadIntradayCandles(newV[0]);
    },
  },
  computed: {
    buyTime() {
      if (this.isBuySellReversed) return this.buySellTimes[1];
      return this.buySellTimes[0];
    },
    sellTime() {
      if (this.isBuySellReversed) return this.buySellTimes[0];
      return this.buySellTimes[1];
    },
  },
  methods: {
    loadIntradayCandles(candle) {
      let from = new Date(candle.time);
      // минус один тик чтобы не взять начальную свечу следующего дня
      let to = new Date(from - 1);
      to.setDate(to.getDate() + 1);

      this.loading = true;
      this.$stockService
        .loadCandles({
          figi: this.instrument.figi,
          interval: this.intervalRequestParam,
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
          this.step = this.interval * 60 * 1000; // 15 минутный шаг
        })
        .finally(() => {
          this.loading = false;
        });
    },

    // форматит дату в "hh:mm"
    formatTooltip(val) {
      let d = new Date(val);
      return `${d
        .getHours()
        .toString()
        .padStart(2, "0")}:${d
        .getMinutes()
        .toString()
        .padStart(2, "0")}`;
    },

    simulate() {
      this.loading = true;
      let buyTime = new Date(this.buyTime);
      let sellTime = new Date(this.sellTime);
      let buySellHours = [buyTime.getHours(), sellTime.getHours()];
      let buySellMinutes = [buyTime.getMinutes(), sellTime.getMinutes()];
      this.$stockService
        .loadCandles({
          figi: this.instrument.figi,
          interval: this.intervalRequestParam,
          from: this.dateRange[0],
          to: this.dateRange[1],
          hours: buySellHours,
          minutes: buySellMinutes,
          format: "json",
        })
        .then((response) => {
          let candles = response.data.results;

          this.startSimulate(candles, buySellHours, buySellMinutes);
        })
        .finally(() => {
          this.loading = false;
        });
    },

    startSimulate(candles, buySellHours, buySellMinutes) {
      this.money = +this.startMoney;
      this.stockCount = 0;
      this.operations = [];
      for (const candle of candles) {
        var time = new Date(candle.time);
        if (
          time.getHours() == buySellHours[0] &&
          time.getMinutes() == buySellMinutes[0]
        )
          this.buy(time, candle.o);
        if (
          time.getHours() == buySellHours[1] &&
          time.getMinutes() == buySellMinutes[1]
        )
          this.sell(time, candle.o);
      }
    },

    buy(time, price) {
      // покупаем на всё
      let lotPrice = price * this.instrument.lot;
      let lotsCanBeBought = Math.trunc(this.money / lotPrice);
      let tradePrice = lotsCanBeBought * lotPrice;
      let tax = this.get_tax(tradePrice);
      let payment = tradePrice + tax;
      let count = lotsCanBeBought * this.instrument.lot;

      this.money = Math.round((this.money - payment) * 100) / 100;
      this.stockCount += count;
      let value =
        Math.round((this.money + this.stockCount * price) * 100) / 100;
      this.operations.push({
        time: time,
        type: "buy",
        count: count,
        price: tradePrice,
        tax: tax,
        value: value,
      });
    },

    sell(time, price) {
      // продаём все
      let lotPrice = price * this.instrument.lot;
      let lotsCanBeSold = this.stockCount / this.instrument.lot;
      let tradePrice = lotsCanBeSold * lotPrice;
      let tax = this.get_tax(tradePrice);
      let refund = tradePrice - tax;
      let count = this.stockCount;

      this.money = Math.round((this.money + refund) * 100) / 100;
      this.stockCount = 0;
      let value =
        Math.round((this.money + this.stockCount * price) * 100) / 100;

      this.operations.push({
        time: time,
        type: "sell",
        count: count,
        price: tradePrice,
        tax: tax,
        value: value,
      });
    },

    get_tax(val) {
      return Math.ceil(val * this.brokerTax) / 100;
    },
  },
};
</script>

<style scoped></style>
