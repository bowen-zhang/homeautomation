<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-switch
          v-model="autoSchedule"
          inset
          label="Auto"
          hide-details
          @change="onChangeAutoSchedule"
        ></v-switch>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-list two-line>
          <v-list-item
            v-for="task in tasks"
            :key="task.zoneId"
            :class="{ active: task.zoneId === runningTask.zoneId }"
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
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" class="text-right">
        <v-btn dark color="green darken-3" @click="onStart" :disabled="tasks.length === 0">Start</v-btn>
        <v-btn @click="onClear" :disabled="tasks.length === 0">Clear</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
module.exports = {
  props: ["irrigationService", "zones", "tasks"],
  data: () => ({
    autoSchedule: null,
    runningTask: {}
  }),
  created() {
    this.refreshTasks();
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
  methods: {
    refreshTasks() {
      this.irrigationService.getCurrentTask(
        new proto.google.protobuf.Empty(),
        {},
        (err, response) => {
          if (response) {
            this.runningTask = response.toObject();
          } else {
            this.runningTask = null;
          }
        }
      );
      this.irrigationService.getPendingTasks(
        new proto.google.protobuf.Empty(),
        {},
        (err, response) => {
          this.tasks.length = 0;
          if (response) {
            response.toObject().tasksList.forEach(x => {
              this.tasks.append(x);
            });
          }
        }
      );
    },
    onChangeAutoSchedule(val) {
      request = new proto.ha.irrigation.AutoScheduleStatus();
      request.setEnabled(val);
      this.irrigationService.setAutoSchedule(request, {}, (err, response) => {
        if (response) {
          this.$emit("notify", `Auto schedule is turned ${val ? "on" : "off"}`);
        } else {
          this.$emit("notify", "Failed to change auto schedule settings.");
        }
      });
    },
    getZone(zoneId) {
      return this.zones.find(x => x.id === zoneId);
    },
    removeTask(task) {
      this.tasks = this.tasks.filter(t => t != task);
    },
    onStart() {
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
          this.$emit("notify", "Task is submitted.");
          setTimeout(this.refreshTasks, 1000);
        } else {
          this.$emit("notify", "Failed to submit task.");
        }
      });
    },
    onClear() {
      this.tasks = [];
      this.irrigationService.submitTasks(
        new proto.ha.irrigation.TaskList(),
        {},
        (err, response) => {
          if (response) {
            this.$emit("notify", "All tasks are cancelled.");
            setTimeout(this.refreshTasks, 1000);
          } else {
            this.$emit("notify", "Failed to cancel tasks.");
          }
        }
      );
    }
  }
};
</script>
<style scoped>
</style>