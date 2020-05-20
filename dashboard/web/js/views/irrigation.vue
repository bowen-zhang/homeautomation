<template>
  <v-container class="pt-0">
    <v-row>
      <v-col cols="12" class="pa-0">
        <div
          class="alert px-2 py-1"
          v-for="alert in alerts"
          :key="alert.getTimestamp().toDate().getTime()"
        >
          {{ formatTimestamp(alert.getTimestamp().toDate()) }}: {{ alert.getMessage() }}
          <v-btn fab x-small @click="dismissAlert(alert)">
            <v-icon x-small>mdi-close</v-icon>
          </v-btn>
        </div>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <rain-dash :weather-service="weatherService"></rain-dash>
      </v-col>
      <v-col cols="12" v-for="zone in zones" :key="zone.id">
        <irrigation-dash :zone="zone" :management-client="irrigationService"></irrigation-dash>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-toolbar dense flat dark color="green darken-3">
            <v-toolbar-title>Schedule</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-switch v-model="autoSchedule" inset label="Auto" hide-details></v-switch>
          </v-toolbar>
          <v-card-text>
            <v-list two-line>
              <v-list-item
                v-for="task in tasks"
                :key="task.zoneId"
                :class="{ active: task.zoneId === currentTask.zoneId }"
              >
                <v-list-item-content>
                  <v-list-item-title>{{ getZone(task.zoneId) === undefined ? task.zoneId : getZone(task.zoneId).name }}</v-list-item-title>
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
              <v-col cols="6" v-for="zone in availableZones" :key="zone.id">
                <v-card @click="addTask(zone.id)" color="green lighten-4">
                  <v-menu bottom left>
                    <template v-slot:activator="{ on }">
                      <v-btn icon v-on="on" class="zone-context-menu">
                        <v-icon medium>mdi-dots-vertical</v-icon>
                      </v-btn>
                    </template>

                    <v-list>
                      <v-list-item @click="editZone(zone)">
                        <v-list-item-title>Edit</v-list-item-title>
                      </v-list-item>
                    </v-list>
                  </v-menu>

                  <v-card-text class="pt-6 pb-2 pr-4">{{ zone.name }}</v-card-text>
                  <v-card-actions></v-card-actions>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
      </v-col>
    </v-row>
    <irrigation-duration ref="irrigationDuration"></irrigation-duration>
    <irrigation-zone-edit ref="irrigationZoneEdit"></irrigation-zone-edit>
    <v-snackbar v-model="showNotification">{{ notificationText }}</v-snackbar>
  </v-container>
</template>
<script>
module.exports = {
  props: ["api"],
  data: () => ({
    irrigationService: null,
    irrigationService: null,
    weatherService: null,
    autoSchedule: null,
    zones: [],
    tasks: [],
    currentTask: {},
    alerts: [],
    showNotification: false,
    notificationText: ""
  }),
  components: {
    "irrigation-dash": httpVueLoader("js/views/irrigation-dash.vue"),
    "irrigation-duration": httpVueLoader("js/views/irrigation-duration.vue"),
    "irrigation-zone-edit": httpVueLoader("js/views/irrigation-zone-edit.vue"),
    "rain-dash": httpVueLoader("js/views/rain-dash.vue")
  },
  created() {
    this.weatherService = new proto.ha.weather.WeatherServiceClient(
      "http://server:17082"
    );
    this.irrigationService = new proto.ha.irrigation.IrrigationServiceClient(
      "http://server:17081"
    );
    this.refreshZones();
    this.refreshTasks();
    this.refreshAlerts();
    this.irrigationService.getAutoSchedule(
      new proto.google.protobuf.Empty(),
      {},
      (err, response) => {
        if (response) {
          this.autoSchedule = response.getEnabled();
        }
      }
    );
  },
  computed: {
    availableZones() {
      return this.zones.filter(
        zone => this.tasks.find(t => t.zoneId == zone.id) === undefined
      );
    }
  },
  watch: {
    autoSchedule(newVal) {
      request = new proto.ha.irrigation.AutoScheduleStatus();
      request.setEnabled(newVal);
      this.irrigationService.setAutoSchedule(request, {}, (err, response) => {
        if (response) {
          this.notify(`Auto schedule is turned ${newVal ? "on" : "off"}`);
        } else {
          this.notify("Failed to change auto schedule settings.");
        }
      });
    }
  },
  methods: {
    refreshZones() {
      this.irrigationService.getAllZones(
        new proto.google.protobuf.Empty(),
        {},
        (err, response) => {
          if (response) {
            this.zones = response.toObject().zonesList;
          } else {
            this.zones = [];
          }
        }
      );
    },
    refreshTasks() {
      this.irrigationService.getCurrentTask(
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
      this.irrigationService.getPendingTasks(
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
    refreshAlerts() {
      const request = new proto.ha.irrigation.GetAlertsRequest();
      request.setMaxCount = 10;
      this.irrigationService.getAlerts(request, {}, (err, response) => {
        if (response) {
          this.alerts = response.getAlertsList();
        } else {
          this.alerts = [];
        }
      });
    },
    getZone(zoneId) {
      return this.zones.find(x => x.id === zoneId);
    },
    addTask(zoneId) {
      this.$refs.irrigationDuration
        .open()
        .then(durationSec => {
          this.tasks.push({
            zoneId: zoneId,
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
          .setZoneId(task.zoneId)
          .setDuration(
            new proto.google.protobuf.Duration().setSeconds(task.durationSec)
          );
      });
      this.irrigationService.submitTasks(tasksToStart, {}, (err, response) => {
        if (response) {
          this.notify("Task is submitted.");
          setTimeout(this.refreshTasks, 1000);
        } else {
          this.notify("Failed to submit task.");
        }
      });
    },
    notify(msg) {
      this.notificationText = msg;
      this.showNotification = true;
    },
    clear() {
      this.tasks = [];
      this.irrigationService.submitTasks(
        new proto.ha.irrigation.TaskList(),
        {},
        (err, response) => {
          if (response) {
            this.notify("All tasks are cancelled.");
            setTimeout(this.refreshTasks, 1000);
          } else {
            this.notify("Failed to cancel tasks.");
          }
          this.showNotification = true;
        }
      );
    },
    editZone(zone) {
      const zoneToEdit = _.cloneDeep(zone);
      this.$refs.irrigationZoneEdit
        .open(zoneToEdit)
        .then(updatedZone => {
          updatedZone = new proto.ha.irrigation.Zone()
            .setId(updatedZone.id)
            .setName(updatedZone.name)
            .setPin(updatedZone.pin)
            .setFlowRateMmpm(updatedZone.flowRateMmpm)
            .setMaxWaterAmountMm(updatedZone.maxWaterAmountMm)
            .setEvaporationRateMmpm(updatedZone.evaporationRateMmpm);
          this.irrigationService.saveZone(updatedZone, {}, (err, response) => {
            if (response) {
              this.notify("Zone is saved.");
              this.refreshZones();
            } else {
              this.notify("Failed to save zone.");
            }
          });
        })
        .catch(() => {});
    },
    formatTimestamp(timestamp) {
      return moment(timestamp).format("YYYY-MM-DD hh:mm:ss");
    },
    dismissAlert(alert) {
      const request = new proto.ha.irrigation.DismissAlertRequest();
      request.setTimestamp(alert.getTimestamp());
      this.irrigationService.dismissAlert(request, {}, (err, response) => {
        this.refreshAlerts();
      });
    }
  }
};
</script>
<style scoped>
.alert {
  background-color: darkred;
  color: white;
}
.active {
  border: solid 2px #43a047;
}
.zone-context-menu {
  position: absolute;
  right: 0px;
  top: 0px;
  color: darkgreen;
  width: 20px;
}
</style>