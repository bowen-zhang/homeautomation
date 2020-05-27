<template>
  <v-dialog
    v-model="dialog"
    max-width="90%"
    style="
       {
        zindex: 200;
      }
    "
    @keydown.esc="cancel"
  >
    <v-card>
      <v-card-title>Zone {{ zone.id }}</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="5">
              <v-text-field label="Group" v-model="zone.group" hide-details></v-text-field>
            </v-col>
            <v-col cols="5">
              <v-text-field label="Name" v-model="zone.name" hide-details></v-text-field>
            </v-col>
            <v-col cols="2">
              <v-text-field label="Pin" v-model="zone.pin" hide-details></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col class="py-0" cols="12">Weekly Water Amount (in)</v-col>
            <v-col class="pt-8 pb-2" cols="12">
              <v-slider
                v-model="totalAmountInPerWeek"
                thumb-label="always"
                min="0"
                max="2.0"
                step="0.1"
                messages="Typical lawn requires 1-1.5in water per week."
              ></v-slider>
            </v-col>
          </v-row>
          <v-row>
            <v-col class="py-0" cols="12">Sprinkler Water Flow (in/h)</v-col>
            <v-col class="pt-8 pb-2" cols="12">
              <v-slider
                v-model="flowRateInPerHour"
                thumb-label="always"
                min="0"
                max="4.0"
                step="0.1"
                messages="Typical sprinkler produces 1.5-2in water per hour."
              ></v-slider>
            </v-col>
          </v-row>
          <v-row>
            <v-col class="py-0" cols="12">Water Interval (days)</v-col>
            <v-col class="pt-8 pb-2" cols="12">
              <v-slider
                v-model="waterIntervalDays"
                thumb-label="always"
                min="1"
                max="30"
                step="1"
                messages="Recommended interval is 3-4 days for lawn, 7-30 days for shrub/trees."
              ></v-slider>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12">{{ message }}
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions class="pt-0">
        <v-spacer></v-spacer>
        <v-btn color="primary darken-1" text @click.native="agree">OK</v-btn>
        <v-btn color="grey" text @click.native="cancel">Cancel</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
module.exports = {
  data: () => ({
    dialog: false,
    zone: {},
    resolve: null,
    reject: null,
    millimeterPerIn: 25.4
  }),
  computed: {
    totalAmountInPerWeek: {
      get() {
        return (
          (this.zone.evaporationRateMmpm * 60 * 24 * 7) / this.millimeterPerIn
        );
      },
      set(newVal) {
        this.zone.evaporationRateMmpm = newVal * this.millimeterPerIn / 60 / 24 / 7;
      }
    },
    flowRateInPerHour: {
      get() {
        return (this.zone.flowRateMmpm * 60) / this.millimeterPerIn;
      },
      set(newVal) {
        this.zone.flowRateMmpm = newVal * this.millimeterPerIn / 60;
      }
    },
    waterIntervalDays: {
      get() {
        return this.zone.maxWaterAmountMm / (this.zone.evaporationRateMmpm * 60 * 24);
      },
      set(newVal) {
        this.zone.maxWaterAmountMm = this.zone.evaporationRateMmpm * 60 * 24 * newVal;
      }
    },
    message() {
      const runMinutes = this.totalAmountInPerWeek / 7 * this.waterIntervalDays / this.flowRateInPerHour * 60;
      return `Current settings will turn on sprinkler for ${runMinutes.toFixed(0)} minutes every ${this.waterIntervalDays.toFixed(0)} days.`;
    }
  },
  methods: {
    open(zone) {
      this.zone = zone;
      this.dialog = true;
      return new Promise((resolve, reject) => {
        this.resolve = resolve;
        this.reject = reject;
      });
    },
    agree() {
      this.dialog = false;
      this.resolve(this.zone);
    },
    cancel() {
      this.dialog = false;
      this.reject();
    }
  }
};
</script>
