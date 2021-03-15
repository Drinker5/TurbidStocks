<template>
  <div v-if="instrument">
    <StockChart :instrument="instrument" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      loading: false,
      instrument: null,
      ticker: this.$route.params.id,
    };
  },
  mounted() {
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
