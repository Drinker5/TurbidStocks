<template>
  <el-row :gutter="10">
    <el-col :span="6">
      <el-form label-width="120px" size="mini">
        <el-form-item label="Lot price">
          <el-input
            placeholder="Lot price"
            v-model="lotPrice"
            type="number"
            :disabled="true"
          >
            <template #suffix>
              {{ instrument.currency }}
            </template>
          </el-input>
        </el-form-item>

        <el-form-item label="Start money">
          <el-input
            placeholder="Start money"
            v-model="startMoney"
            type="number"
            :min="lotPrice"
          >
            <template #suffix>
              {{ instrument.currency }}
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="Broker tax %">
          <el-input-number
            v-model="brokerTax"
            :precision="3"
            :step="0.05"
            :min="0"
            :max="5"
            placeholder="Broker tax %"
          >
          </el-input-number>
        </el-form-item>
        <el-form-item label="Candle interval">
          <el-select v-model="interval" placeholder="Select interval">
            <el-option
              v-for="item in intervalOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="Buy-sell times">
          <el-row :gutter="5">
            <el-col :span="12">Buy time {{ formatTooltip(buyTime) }}</el-col>
            <el-col :span="12">Sell time {{ formatTooltip(sellTime) }}</el-col>
          </el-row>
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
          <el-checkbox v-model="isBuySellReversed"
            >Reverse buy/sell</el-checkbox
          >
        </el-form-item>

        <el-form-item label="Buy option">
          <el-radio-group v-model="buyOption">
            <el-radio-button label="Open" name="buyOption"></el-radio-button>
            <el-radio-button label="High" name="buyOption"></el-radio-button>
            <el-radio-button label="Low" name="buyOption"></el-radio-button>
            <el-radio-button label="Close" name="buyOption"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="Sell option">
          <el-radio-group v-model="sellOption">
            <el-radio-button label="Open" name="sellOption"></el-radio-button>
            <el-radio-button label="High" name="sellOption"></el-radio-button>
            <el-radio-button label="Low" name="sellOption"></el-radio-button>
            <el-radio-button label="Close" name="sellOption"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="simulate">
            Simulate
          </el-button>
        </el-form-item>
        <el-form-item label="Trading days" v-if="operations.length">
          {{ candles.length }}
        </el-form-item>
        <el-form-item label="Tades" v-if="operations.length">
          {{ operations.length }}
        </el-form-item>
        <el-form-item label="Tax total" v-if="operations.length">
          {{ taxTotal() }} {{ instrument.currency }}
        </el-form-item>
        <el-form-item label="Profit" v-if="operations.length">
          {{ profit() }} {{ instrument.currency }}
        </el-form-item>
        <el-form-item label="Performance" v-if="operations.length">
          {{ performance() }}%
        </el-form-item>
      </el-form>
    </el-col>

    <el-col :span="18">
      <StockChart
        :instrument="instrument"
        :loading="loading"
        :candles="candles"
      />

      <SimulatorReview
        :operations="operations"
        :loading="loading"
        :instrument="instrument"
      />
    </el-col>
  </el-row>
</template>

<script>
import moment from "moment";

export default {
  props: {
    instrument: Object,
    candles: Array,
    dateRange: Array,
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
      isBuySellReversed: false,
      lotPrice: 0,
      buyOption: "Open",
      sellOption: "Open",
      interval: 15,
      intervalOptions: [
        { value: 1, label: "1min", step: "00:01" },
        { value: 5, label: "5min", step: "00:05" },
        { value: 10, label: "10min", step: "00:10" },
        { value: 15, label: "15min", step: "00:15" },
        { value: 30, label: "30min", step: "00:30" },
      ],
    };
  },
  mounted() {},
  watch: {
    candles(newV) {
      this.loadIntradayCandles(newV[0]);
      this.lotPrice = newV[0].o * this.instrument.lot;
    },
  },
  computed: {
    intervalRequestParam() {
      return `${this.interval}min`;
    },
    step() {
      return this.interval * 60 * 1000;
    },
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
    getOptionValue(optionName) {
      switch (optionName) {
        case "Open":
          return "o";
        case "High":
          return "h";
        case "Low":
          return "l";
        case "Close":
          return "c";
      }

      return "o";
    },

    startSimulate(candles, buySellHours, buySellMinutes) {
      this.money = +this.startMoney;
      this.stockCount = 0;
      this.operations = [];
      let b = this.getOptionValue(this.buyOption);
      let s = this.getOptionValue(this.sellOption);
      for (const candle of candles) {
        var time = new Date(candle.time);
        if (
          time.getHours() == buySellHours[0] &&
          time.getMinutes() == buySellMinutes[0]
        )
          this.buy(time, candle[b]);
        if (
          time.getHours() == buySellHours[1] &&
          time.getMinutes() == buySellMinutes[1]
        )
          this.sell(time, candle[s]);
      }
    },

    buy(time, price) {
      // покупаем на всё
      let lotPrice = price * this.instrument.lot;
      let lotsCanBeBought = Math.trunc(this.money / lotPrice);
      let tradePrice = lotsCanBeBought * lotPrice;
      let tax = this.getTax(tradePrice);
      let payment = tradePrice + tax;
      let count = lotsCanBeBought * this.instrument.lot;
      if (count <= 0) return;
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
      if (this.stockCount <= 0) return;
      // продаём все
      let lotPrice = price * this.instrument.lot;
      let lotsCanBeSold = this.stockCount / this.instrument.lot;
      let tradePrice = lotsCanBeSold * lotPrice;
      let tax = this.getTax(tradePrice);
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

    getTax(val) {
      return Math.ceil(val * this.brokerTax) / 100;
    },

    taxTotal() {
      if (this.operations.length <= 0) return;
      let result = this.operations.reduce((a, b) => {
        return { tax: a.tax + b.tax };
      }).tax;
      return Math.round(result * 100) / 100;
    },
    profit() {
      if (this.operations.length <= 0) return;
      let lastOperation = this.operations[this.operations.length - 1];
      let result = lastOperation.value - this.startMoney;
      return Math.round(result * 100) / 100;
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

<style scoped></style>
