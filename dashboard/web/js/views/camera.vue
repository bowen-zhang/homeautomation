<template>
  <div class="cameraView">
    <div class="title">{{ node.name }}</div>
    <img class="image" :src="url" />
  </div>
</template>
<script>
module.exports = {
  props: ["node"],
  data: () => ({}),
  computed: {
    url() {
      if (!this.node) {
        return null;
      }
      return `http://${this.node.ip}:${this.node.httpPort}/video`;
    }
  },
  created() {},
  methods: {}
};
</script>
<style scoped>
.cameraView {
  position: relative;
}
.title {
  position: absolute;
  top: 0px;
  left: 0px;
  background-color: rgba(255, 255, 255, 0.5);
  padding: 4px 4px 4px 4px;
  line-height: 1em;
  border-bottom-right-radius: 6px;
}
.image {
  display: block;
  width: 100%;
  height: auto;
}
</style>