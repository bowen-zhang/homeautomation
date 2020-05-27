<template>
  <div>
    <v-tabs v-model="tab" dark background-color="green darken-3" grow>
      <v-tab key="zones">Zones</v-tab>
      <v-tab key="tasks">
        <v-badge :content="`${tasks.length}`" color="red" dark>Tasks</v-badge>
      </v-tab>
      <v-tab key="alerts">
        <v-badge :content="`${alerts.length}`" color="red" dark>Alerts</v-badge>
      </v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item key="zones">
        <irrigation-zone-view
          :irrigation-service="irrigationService"
          :zones="zones"
          @newtask="onNewTask"
          @notify="onNotify"
          @refresh="onRefreshZones"
        ></irrigation-zone-view>
      </v-tab-item>
      <v-tab-item key="tasks">
        <irrigation-task-view
          :irrigation-service="irrigationService"
          :zones="zones"
          :tasks="tasks"
          @notify="onNotify"
        ></irrigation-task-view>
      </v-tab-item>
      <v-tab-item key="alerts">
        <v-container>
          <v-row>
            <v-col
              cols="12"
              class="alert px-2 py-1"
              v-for="alert in alerts"
              :key="alert.getTimestamp().toDate().getTime()"
            >
              {{ formatTimestamp(alert.getTimestamp().toDate()) }}: {{ alert.getMessage() }}
              <v-btn fab x-small @click="dismissAlert(alert)">
                <v-icon x-small>mdi-close</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-tab-item>
    </v-tabs-items>
    <v-snackbar v-model="showNotification">{{ notificationText }}</v-snackbar>
  </div>
</template>
<script>
module.exports = {
  props: ["api"],
  data: () => ({
    irrigationService: null,
    tab: "zones",
    zones: [],
    selectedZone: null,
    tasks: [],
    alerts: [],
    showNotification: false,
    notificationText: ""
  }),
  components: {
    "irrigation-zone-view": httpVueLoader("js/views/irrigation-zone-view.vue"),
    "irrigation-task-view": httpVueLoader("js/views/irrigation-task-view.vue")
  },
  created() {
    this.irrigationService = new proto.ha.irrigation.IrrigationServiceClient(
      `http://${location.hostname}:17081`
    );
    this.refreshZones();
    this.refreshAlerts();
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
    notify(msg) {
      this.notificationText = msg;
      this.showNotification = true;
    },
    onNewTask(task) {
      this.tasks.push(task);
    },
    onRefreshZones() {
      this.refreshZones();
    },
    onNotify(msg) {
      this.notify(msg);
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
</style>