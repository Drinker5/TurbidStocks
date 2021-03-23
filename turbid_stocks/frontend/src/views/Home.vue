<template>
  <el-container>
    <el-main>
      <el-form :inline="true" label-width="120px" size="mini">
        <el-form-item label="Instument">
          <InstrumentPicker @select="select" />
        </el-form-item>

        <el-form-item label="Date range">
          <DateRangePicker />
        </el-form-item>
      </el-form>
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
