<template>
  <el-progress
    v-if="showProgress"
    :text-inside="true"
    :stroke-width="20"
    :percentage="100 * percentage"
    status="warning"
  >
    <span>{{ positionDate }}</span>
  </el-progress>
</template>

<script>
import moment from "moment";

export default {
  data() {
    return {
      connection: null,
      showProgress: false,
      position: 0.5,
      startPosition: 0,
      endPosition: 1,
    };
  },
  methods: {
    sendMessage: function(message) {
      console.log(this.connection);
      this.connection.send(
        JSON.stringify({
          message: message,
        })
      );
    },
  },
  computed: {
    percentage() {
      return (
        (this.position - this.startPosition) /
        (this.endPosition - this.startPosition)
      );
    },
    positionDate() {
      return moment(this.position).format("DD.MM.YYYY");
    },
  },
  created() {
    this.connection = new WebSocket(`ws://${window.location.host}/ws/stock/`);

    this.connection.onmessage = (event) => {
      const data = JSON.parse(event.data);
      switch (data.type) {
        case "start":
          this.showProgress = true;
          var from = new Date(data.from);
          this.position = from.getTime();
          this.startPosition = from.getTime();
          var to = new Date(data.to);
          this.endPosition = to.getTime();
          break;
        case "progress":
          this.position = new Date(data.position).getTime();
          break;
        case "end":
          this.showProgress = false;
          break;
      }
    };

    // this.connection.onopen = (event) => {};
  },
};
</script>

<style></style>
