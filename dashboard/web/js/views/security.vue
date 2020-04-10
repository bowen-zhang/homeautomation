<template>
  <v-container py-0>
    <v-row>
      <v-col
        :cols="cols"
        class="cameraViewHolder"
        v-for="node in nodes"
        :key="node.id"
        v-show="node.lastHeartbeat"
      >
        <camera :node="node"></camera>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
module.exports = {
  props: ["api"],
  data: () => ({
    nodes: []
  }),
  computed: {
    cols() {
      const r = Math.sqrt(this.nodes.length);
      return 12 / Math.ceil(r);
    }
  },
  components: {
    camera: httpVueLoader("js/views/camera.vue")
  },
  mounted() {
    this.api.getSecurityConfig(config => {
      console.log(config);
      this.nodes = config.nodes
        .filter(
          n =>
            n.lastHeartbeatTimestamp !== undefined &&
            n.components !== undefined &&
            n.components.some(c => c.httpServer !== undefined) &&
            n.components.some(c => c.videoStreamer !== undefined)
        )
        .map(n => ({
          id: n.id,
          name: n.name,
          ip: n.ip,
          httpPort: n.components.find(c => c.httpServer !== undefined)
            .httpServer.port,
          lastHeartbeat: this.timestampToDate(n.lastHeartbeatTimestamp)
        }));
      console.log(this.nodes);
    });
  },
  methods: {
    timestampToDate(ts) {
      if (ts === undefined || !ts) {
        return null;
      }
      return new Date(ts);
    }
  }
};
</script>
<style scoped>
.cameraViewHolder {
  padding: 0px 0px 0px 0px;
}
</style>