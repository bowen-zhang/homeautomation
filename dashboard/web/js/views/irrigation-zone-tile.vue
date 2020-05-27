<template>
  <v-card :color="selected ? 'green lighten-2' : 'green lighten-4'">
    <v-card-title class="subtitle-1 pa-2 pb-0">{{ zone.name }}</v-card-title>
    <v-card-text class="pa-0">
      <apexchart
        class="water-level"
        type="radialBar"
        height="120"
        :options="options"
        :series="[waterLevelPercentage]"
      ></apexchart>
      <p class="mb-0">{{ status }}</p>
    </v-card-text>
    <v-card-actions class="pt-0">
      <v-btn icon small @click="onWater">
        <v-icon>mdi-sprinkler-variant</v-icon>
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn icon small @click="onEdit">
        <v-icon>mdi-cog-outline</v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>
<script>
module.exports = {
  props: ["irrigationService", "zone", "selected"],
  data: () => ({
    info: null,
    options: {
      colors: ["#dbd87f"],
      plotOptions: {
        radialBar: {
          startAngle: -90,
          endAngle: 90,
          track: {
            background: "#333",
            startAngle: -90,
            endAngle: 90
          },
          dataLabels: {
            name: {
              show: false
            },
            value: {
              fontSize: "14px",
              show: true,
              offsetY: -5,
              formatter: x => x.toFixed(0) + "%"
            }
          }
        }
      },
      fill: {
        type: "gradient",
        gradient: {
          shade: "dark",
          type: "horizontal",
          gradientToColors: ["#20E647"],
          stops: [0, 100]
        }
      },
      stroke: {
        lineCap: "butt"
      },
      labels: ["Progress"]
    }
  }),
  watch: {
    zone: {
      handler(newVal) {
        this.refreshZoneInfo();
      },
      immediate: true
    }
  },
  computed: {
    waterLevelPercentage() {
      if (!this.zone || !this.info || this.zone.maxWaterAmountMm === 0) {
        return 0;
      }

      return Math.min(
        100,
        (100.0 * this.info.currentWaterLevelMm) / this.zone.maxWaterAmountMm
      );
    },
    status() {
      if (!this.info || this.info.lastRunTime.seconds === 0) {
        return null;
      }

      const lastRunTime = new Date(this.info.lastRunTime.seconds * 1000);
      return `Last watered ${moment(lastRunTime).fromNow()}.`;
    }
  },
  methods: {
    refreshZoneInfo() {
      const request = new proto.ha.irrigation.GetZoneInfoRequest();
      request.setZoneId(this.zone.id);
      this.irrigationService.getZoneInfo(request, {}, (err, response) => {
        this.info = response.toObject();
      });
    },
    onWater() {
      this.$emit("water");
    },
    onEdit() {
      this.$emit("edit");
    }
  }
};
</script>
<style scoped>
.water-level {
  position: relative;
  top: -15px;
  margin-bottom: -25px;
}
</style>