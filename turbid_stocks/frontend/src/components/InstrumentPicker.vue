<template>
  <el-form label-width="120px" size="mini">
    <el-form-item label="Instument">
      <el-select
        v-model="ticker"
        filterable
        remote
        :remote-method="remoteMethod"
        :loading="loading"
        @change="change"
      >
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.name"
          :value="item.ticker"
        >
          <el-row :gutter="20">
            <el-col :span="4">
              <el-avatar size="small" :src="item.icon_url"></el-avatar>
            </el-col>
            <el-col
              :span="16"
              style="text-overflow: ellipsis; overflow: hidden;"
            >
              {{ item.name }}
            </el-col>

            <el-col :span="4">
              <span style="float: right; color: #8492a6; font-size: 13px">
                {{ item.ticker }}
              </span>
            </el-col>
          </el-row>
        </el-option>
      </el-select>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  data() {
    return {
      loading: false,
      options: [],
      ticker: this.$route.params.id,
    };
  },
  mounted() {
    this.remoteMethod("");
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
          this.options = response.data.results;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    change(ticker) {
      this.$emit("select", ticker);
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
