<template>
  <Progress />
  <div v-if="instrument">
    <Simulator />
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  data() {
    return {
      loading: false,
      ticker: this.$route.params.id,
    };
  },
  mounted() {
    this.loadInstrument();
  },
  watch: {},
  computed: mapState(["instrument"]),
  methods: {
    loadInstrument() {
      this.loading = true;
      this.$stockService
        .loadInstrument(this.ticker)
        .then((response) => {
          this.$store.commit("setInstrument", response.data);
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>

<style></style>
