<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-select
          :items="stations"
          label="Station"
          v-model="selectedStationId"
          item-text="name"
          item-value="id"
        ></v-select>
      </v-col>
      <v-col cols="12">
        <v-slider
          v-model="durationMin"
          min="1"
          max="15"
          hide-details
          thumb-label="always"
          label="Duration (min)"
        ></v-slider>
      </v-col>
      <v-col>
        <v-btn @click="run()">Run</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6" v-for="station in stations" :key="station.id">
        <v-card :class="{ active: station.id === currentTask.stationId }">
          <v-card-text>{{ station.name }}</v-card-text>
          <v-card-actions></v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <ul>
          <li
            v-for="task in tasks"
            :key="task.stationId"
          >{{ task.stationId }}: {{ task.durationSec }}</li>
        </ul>
      </v-col>
    </v-row>
    <v-snackbar v-model="showNotification">{{ notificationText }}</v-snackbar>
  </v-container>
</template>
<script>
module.exports = {
  props: ["api"],
  data: () => ({
    client: null,
    stations: [],
    tasks: [],
    currentTask: {},
    selectedStationId: -1,
    durationMin: 10,
    showNotification: false,
    notificationText: ""
  }),
  created() {
    this.client = new proto.ha.irrigation.IrrigationServiceClient(
      "http://server:17080"
    );
    this.client.getConfig(
      new proto.google.protobuf.Empty(),
      {},
      (err, response) => {
        if (response) {
          this.stations = response.toObject().stationsList;
        } else {
          this.stations = [];
        }
      }
    );
    this.refreshTasks();
  },
  methods: {
    refreshTasks() {
      this.client.getCurrentTask(
        new proto.google.protobuf.Empty(),
        {},
        (err, response) => {
          if (response) {
            this.currentTask = response.toObject();
          } else {
            this.currentTask = null;
          }
        }
      );
      this.client.getPendingTasks(
        new proto.google.protobuf.Empty(),
        {},
        (err, response) => {
          if (response) {
            this.tasks = response.toObject().tasksList;
          } else {
            this.tasks = [];
          }
        }
      );
    },
    run() {
      const tasks = new proto.ha.irrigation.TaskList();
      tasks
        .addTasks()
        .setStationId(this.selectedStationId)
        .setDurationSec(this.durationMin * 60);
      this.client.submitTasks(tasks, {}, (err, response) => {
        if (response) {
          this.notificationText = "Task is submitted.";
          setTimeout(this.refreshTasks, 1000);
        } else {
          this.notificationText = "Failed to submit task.";
        }
        this.showNotification = true;
      });
    }
  }
};
</script>
<style scoped>
.active {
  background-color: #0277bd;
}
.active .v-card__text {
  color: white;
}
</style>