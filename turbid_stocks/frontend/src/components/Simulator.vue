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
        <el-form-item label="Commission %">
          <el-input-number
            v-model="brokerCommission"
            :precision="3"
            :step="0.05"
            :min="0"
            :max="5"
            placeholder="Broker commission %"
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
          <el-checkbox v-model="isBuySellReversed">
            Reverse buy/sell
          </el-checkbox>
        </el-form-item>

        <el-form-item label="Buy price">
          <el-radio-group v-model="buyPrice">
            <el-radio-button label="Open" name="buyPrice"></el-radio-button>
            <el-radio-button label="High" name="buyPrice"></el-radio-button>
            <el-radio-button label="Low" name="buyPrice"></el-radio-button>
            <el-radio-button label="Close" name="buyPrice"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="Sell price">
          <el-radio-group v-model="sellPrice">
            <el-radio-button label="Open" name="sellPrice"></el-radio-button>
            <el-radio-button label="High" name="sellPrice"></el-radio-button>
            <el-radio-button label="Low" name="sellPrice"></el-radio-button>
            <el-radio-button label="Close" name="sellPrice"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="Buy days">
          <el-checkbox-group v-model="buyDays">
            <el-checkbox-button
              v-for="(day, index) in ['M', 'T', 'W', 'T', 'F', 'S', 'S']"
              :label="index + 1"
              v-bind:key="index"
            >
              {{ day }}
            </el-checkbox-button>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="Sell days">
          <el-checkbox-group v-model="sellDays">
            <el-checkbox-button
              v-for="(day, index) in ['M', 'T', 'W', 'T', 'F', 'S', 'S']"
              :label="index + 1"
              v-bind:key="index"
            >
              {{ day }}
            </el-checkbox-button>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="simulate">
            Simulate
          </el-button>
        </el-form-item>
        <el-form-item label="Trading days" v-if="operations.length">
          {{ dayCandles.length }}
        </el-form-item>
        <el-form-item label="Tades" v-if="operations.length">
          {{ operations.length }}
        </el-form-item>
        <el-form-item label="Commission total" v-if="operations.length">
          {{ commissionTotal }} {{ instrument.currency }}
        </el-form-item>
        <el-form-item label="Profit" v-if="operations.length">
          {{ profit }} {{ instrument.currency }}
        </el-form-item>
        <el-form-item label="Performance" v-if="operations.length">
          {{ performance }}%
        </el-form-item>

        <OperationList />
      </el-form>
    </el-col>

    <el-col :span="18">
      <StockChart :loading="loading" />
      <GroupCandlesChart />
      <ReviewChart :operations="operations" :loading="loading" />
    </el-col>
  </el-row>
</template>

<script>
import { mapState } from "vuex";
import Simulator from "../plugins/simulator";

export default {
  props: {},
  components: {},

  data() {
    return {
      loading: false,
      brokerCommission: 0.05,
      startMoney: 1000.0,
      buySellTimes: [(7 * 60 + 30) * 60 * 1000, 18 * 60 * 60 * 1000],
      minTime: 7 * 60 * 60 * 1000,
      maxTime: 23 * 60 * 60 * 1000,
      isBuySellReversed: true,
      lotPrice: 0,
      buyPrice: "Open",
      sellPrice: "Open",
      intervalOptions: [
        { value: 1, label: "1min" },
        { value: 5, label: "5min" },
        { value: 10, label: "10min" },
        { value: 15, label: "15min" },
        { value: 30, label: "30min" },
        { value: 60, label: "hour" },
      ],
      buyDays: [1, 2, 3, 4, 5],
      sellDays: [1, 2, 3, 4, 5],
      operations: [],
      commissionTotal: 0,
      profit: 0,
      performance: 0,
    };
  },
  mounted() {
    this.loadDayCandles();
  },
  watch: {
    dateRange() {
      this.loadDayCandles();
    },
    dayCandles(newV) {
      if (newV.length <= 0) return;
      this.loadIntradayCandles(newV[0]);
      this.lotPrice = newV[0].o * this.instrument.lot;
    },
  },
  computed: {
    interval: {
      get() {
        return this.$store.state.interval;
      },
      set(value) {
        this.$store.commit("setInterval", value);
      },
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
    ...mapState(["instrument", "dateRange", "dayCandles"]),
    sellDayFlags() {
      var res = 0;
      for (let day of this.sellDays) {
        res |= 1 << (day - 1);
      }

      return res;
    },
    buyDayFlags() {
      var res = 0;
      for (let day of this.buyDays) {
        res |= 1 << (day - 1);
      }

      return res;
    },
  },
  methods: {
    loadDayCandles() {
      if (!this.dateRange) return;
      this.loading = true;
      this.$stockService
        .loadCandles({
          figi: this.instrument.figi,
          interval: "day",
          from: this.dateRange[0],
          to: this.dateRange[1],
        })
        .then((response) => {
          this.$store.commit("setDayCandles", response.data.results);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    loadIntradayCandles(candle) {
      let from = new Date(candle.time);
      // минус один тик чтобы не взять начальную свечу следующего дня
      let to = new Date(from - 1);
      to.setDate(to.getDate() + 1);

      this.loading = true;
      this.$stockService
        .loadCandles({
          figi: this.instrument.figi,
          interval: this.$store.getters.intervalRequestParam,
          from: from,
          to: to,
          format: "json",
        })
        .then((response) => {
          let intradayCandles = response.data.results;
          if (intradayCandles.length <= 0) return;
          let startDate = new Date(intradayCandles[0].time);

          // добавим сдвиг чтобы попасть в UTC
          let base = startDate.setHours(
            0,
            -startDate.getTimezoneOffset(),
            0,
            0
          );

          let l = new Date(intradayCandles[0].time).getTime();
          let r = new Date(
            intradayCandles[intradayCandles.length - 1].time
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
          interval: this.$store.getters.intervalRequestParam,
          from: this.dateRange[0],
          to: this.dateRange[1],
          hours: buySellHours,
          minutes: buySellMinutes,
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
      const simulator = new Simulator();
      simulator
        .setLotSize(this.instrument.lot)
        .setStartMoney(+this.startMoney)
        .setBrokerCommission(this.brokerCommission);

      let b = this.getOptionValue(this.buyPrice);
      let s = this.getOptionValue(this.sellPrice);
      for (const candle of candles) {
        var time = new Date(candle.time);
        var weekdayflag = 1 << (time.getUTCDay() - 1);
        if (
          time.getHours() == buySellHours[0] &&
          time.getMinutes() == buySellMinutes[0] &&
          (this.buyDayFlags & weekdayflag) > 0
        )
          simulator.buy(time, candle[b]);
        if (
          time.getHours() == buySellHours[1] &&
          time.getMinutes() == buySellMinutes[1] &&
          (this.sellDayFlags & weekdayflag) > 0
        )
          simulator.sell(time, candle[s]);
      }

      this.operations = simulator.operations;
      this.commissionTotal = simulator.commissionTotal;
      this.profit = simulator.profit;
      this.performance = simulator.performance;
    },
  },
};
</script>

<style scoped></style>
