<template>
  <el-select
    v-model="ticker"
    filterable
    remote
    :remote-method="remoteMethod"
    :loading="loading"
  >
    <el-option
      v-for="item in options"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    >
    </el-option>
  </el-select>
  {{ ticker }}
</template>

<script>
export default {
  props: {},
  data() {
    return {
      loading: false,
      options: [],
      ticker: null,
    };
  },
  methods: {
    remoteMethod(query) {
      this.loading = true;
      this.axios
        .get("/api/instruments/", {
          params: {
            search: query,
            format: "json",
          },
        })
        .then((response) => {
          this.options = response.data.results.map((i) => {
            return { value: i.ticker, label: i.name };
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
