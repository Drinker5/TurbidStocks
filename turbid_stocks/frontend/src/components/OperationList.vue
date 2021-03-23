<template>
  <el-space direction="vertical">
    <el-card v-for="i in operations" :key="i.time">
      {{ i.type }} {{ i.count }}
      <span :class="i.type">{{ i.change }}</span>
      <div class="bottom">
        <time>{{ formatDate(i.time) }}</time>
        Tax: {{ i.tax }}
      </div>
    </el-card>
  </el-space>
</template>

<script>
import moment from "moment";
export default {
  props: {
    operations: Array,
  },
  methods: {
    formatDate(date) {
      return moment(date).format("DD.MM.YYYY HH:mm");
    },
  },
};
</script>

<style scoped>
.bottom {
  font-size: 13px;
  color: #999;
}
.sell {
  color: #494;
}
</style>
