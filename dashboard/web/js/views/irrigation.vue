<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-toolbar dense flat dark color="green darken-3">
            <v-toolbar-title>Schedule</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-list two-line>
              <v-list-item
                v-for="task in tasks"
                :key="task.stationId"
                :class="{ active: task.stationId === currentTask.stationId }"
              >
                <v-list-item-content>
                  <v-list-item-title>{{ getStation(task.stationId) === undefined ? task.stationId : getStation(task.stationId).name }}</v-list-item-title>
                  <v-list-item-subtitle>{{ Math.round(task.durationSec/60,1) }} minutes</v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-icon>
                  <v-icon @click="removeTask(task)">mdi-trash-can-outline</v-icon>
                </v-list-item-icon>
              </v-list-item>
            </v-list>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn dark color="green darken-3" @click="start()" :disabled="tasks.length === 0">Start</v-btn>
            <v-btn @click="clear()" :disabled="tasks.length === 0">Clear</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-toolbar dense flat dark color="green darken-3">
            <v-toolbar-title>Zones</v-toolbar-title>
          </v-toolbar>
          <v-container>
            <v-row>
              <v-col cols="6" v-for="station in availableStations" :key="station.id">
                <v-card @click="addTask(station.id)" color="green lighten-4">
                  <v-card-text>{{ station.name }}</v-card-text>
                  <v-card-actions></v-card-actions>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
      </v-col>
    </v-row>
    <irrigation-duration ref="irrigationDuration"></irrigation-duration>
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
    showNotification: false,
    notificationText: ""
  }),
  components: {
    "irrigation-duration": httpVueLoader("js/views/irrigation-duration.vue")
  },
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
  computed: {
    availableStations() {
      return this.stations.filter(
        station => this.tasks.find(t => t.stationId == station.id) === undefined
      );
    }
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
    getStation(stationId) {
      return this.stations.find(x => x.id === stationId);
    },
    addTask(stationId) {
      this.$refs.irrigationDuration
        .open()
        .then(durationSec => {
          this.tasks.push({
            stationId: stationId,
            durationSec: durationSec
          });
        })
        .catch(() => {});
    },
    removeTask(task) {
      this.tasks = this.tasks.filter(t => t != task);
    },
    start() {
      const tasksToStart = new proto.ha.irrigation.TaskList();
      this.tasks.forEach(task => {
        tasksToStart
          .addTasks()
          .setStationId(task.stationId)
          .setDurationSec(task.durationSec);
      });
      this.client.submitTasks(tasksToStart, {}, (err, response) => {
        if (response) {
          this.notificationText = "Task is submitted.";
          setTimeout(this.refreshTasks, 1000);
        } else {
          this.notificationText = "Failed to submit task.";
        }
        this.showNotification = true;
      });
    },
    clear() {
      this.tasks = [];
      this.client.submitTasks(
        new proto.ha.irrigation.TaskList(),
        {},
        (err, response) => {
          if (response) {
            this.notificationText = "All tasks are cancelled.";
            setTimeout(this.refreshTasks, 1000);
          } else {
            this.notificationText = "Failed to cancel tasks.";
          }
          this.showNotification = true;
        }
      );
    }
  }
};
</script>
<style scoped>
.active {
  border: solid 2px #43a047;
}
</style>