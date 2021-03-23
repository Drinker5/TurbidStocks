<template>
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
</template>

<script>
export default {
  data() {
    return {
      defaultTime: [
        new Date(2000, 1, 1, 0, 0, 0),
        new Date(2000, 2, 1, 0, 0, 0),
      ],
      disabledDate(time) {
        return time.getTime() > Date.now();
      },
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
    };
  },
  watch: {},
  computed: {
    dateRange: {
      get() {
        return this.$store.state.dateRange;
      },
      set(value) {
        this.$store.commit("setDateRange", value);
      },
    },
  },
  mounted() {
    let x = new Date();
    this.dateRange = [
      new Date(x.getFullYear() - 1, x.getMonth(), x.getDate()),
      new Date(x.getFullYear(), x.getMonth(), x.getDate()),
    ];
  },
  methods: {},
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
