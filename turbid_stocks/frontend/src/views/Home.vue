<template>
  <InstrumentPicker @select="select" />
  <router-view :key="$route.fullPath" />
</template>

<script>
export default {
  methods: {
    select(ticker) {
      this.$router.push({ name: "stock", params: { id: ticker } });
    },
  },
};
</script>
