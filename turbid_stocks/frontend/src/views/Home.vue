<template>
  <el-container>
    <el-main>
      <InstrumentPicker @select="select" />
      <router-view :key="$route.fullPath" />
    </el-main>
  </el-container>
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
