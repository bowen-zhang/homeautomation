<template>
  <v-container>
    <v-row class="height:375px">
      <v-col cols="12" v-if="!selectedZone">
        <rain-dash :weather-service="weatherService"></rain-dash>
      </v-col>
      <v-col cols="12" v-if="selectedZone">
        <irrigation-dash :zone="selectedZone" :management-client="irrigationService"></irrigation-dash>
      </v-col>
    </v-row>
    <v-row class="px-2" v-for="group in groups" :key="group">
      <v-col cols="12" class="pa-2">{{ group }}</v-col>
      <v-col
        cols="6"
        class="pa-2"
        v-for="zone in zones.filter(x => x.group === group)"
        :key="zone.id"
        @click="onSelectZone(zone)"
      >
        <irrigation-zone-tile
          :irrigation-service="irrigationService"
          :zone="zone"
          :selected="zone===selectedZone"
          @water="onWaterZone(zone)"
          @edit="onEditZone(zone)"
        ></irrigation-zone-tile>
      </v-col>
    </v-row>
    <irrigation-duration ref="irrigationDuration"></irrigation-duration>
    <irrigation-zone-edit ref="irrigationZoneEdit"></irrigation-zone-edit>
  </v-container>
</template>
<script>
module.exports = {
  props: ["irrigationService", "zones"],
  data: () => ({
    weatherService: null,
    selectedZone: null
  }),
  components: {
    "irrigation-duration": httpVueLoader("js/views/irrigation-duration.vue"),
    "irrigation-zone-tile": httpVueLoader("js/views/irrigation-zone-tile.vue"),
    "irrigation-zone-edit": httpVueLoader("js/views/irrigation-zone-edit.vue"),
    "irrigation-dash": httpVueLoader("js/views/irrigation-dash.vue"),
    "rain-dash": httpVueLoader("js/views/rain-dash.vue")
  },
  created() {
    this.weatherService = new proto.ha.weather.WeatherServiceClient(
      `http://${location.hostname}:17082`
    );
  },
  computed: {
    groups() {
      return new Set(this.zones.map(x => x.group));
    }
  },
  methods: {
    onWaterZone(zone) {
      this.$refs.irrigationDuration
        .open()
        .then(durationSec => {
          this.$emit("newtask", {
            zoneId: zone.id,
            durationSec: durationSec
          });
        })
        .catch(() => {});
    },
    onEditZone(zone) {
      const zoneToEdit = _.cloneDeep(zone);
      this.$refs.irrigationZoneEdit
        .open(zoneToEdit)
        .then(updatedZone => {
          console.log("updated");
          updatedZone = new proto.ha.irrigation.Zone()
            .setId(updatedZone.id)
            .setName(updatedZone.name)
            .setGroup(updatedZone.group)
            .setPin(updatedZone.pin)
            .setFlowRateMmpm(updatedZone.flowRateMmpm)
            .setMaxWaterAmountMm(updatedZone.maxWaterAmountMm)
            .setEvaporationRateMmpm(updatedZone.evaporationRateMmpm);
          console.log(updatedZone);
          this.irrigationService.saveZone(updatedZone, {}, (err, response) => {
            if (response) {
              this.$emit("notify", "Zone is saved.");
              this.$emit("refresh");
            } else {
              this.$emit("notify", "Failed to save zone.");
            }
          });
        })
        .catch(error => {
          console.log(error);
        });
    },
    onSelectZone(zone) {
      if (this.selectedZone === zone) {
        this.selectedZone = null;
      } else {
        this.selectedZone = zone;
      }
    }
  }
};
</script>