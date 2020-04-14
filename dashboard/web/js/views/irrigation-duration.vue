<template>
  <v-dialog v-model="dialog" max-width="90%" style="{ zIndex: 200 }" @keydown.esc="cancel">
    <v-card>
      <v-card-title>Run for...</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" align="center" justify="center">
              <v-btn @click="minus()">
                <v-icon>mdi-minus</v-icon>
              </v-btn>
              <span class="subtitle-1 pa-2">{{ durationMin }} minutes</span>
              <v-btn @click="plus()">
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </v-col>
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
    durationMin: 5,
    resolve: null,
    reject: null
  }),
  methods: {
    open() {
      this.dialog = true;
      return new Promise((resolve, reject) => {
        this.resolve = resolve;
        this.reject = reject;
      });
    },
    plus() {
      this.durationMin += 1;
    },
    minus() {
      this.durationMin = Math.max(1, this.durationMin - 1);
    },
    agree() {
      this.dialog = false;
      this.resolve(this.durationMin * 60);
    },
    cancel() {
      this.dialog = false;
      this.reject();
    }
  }
};
</script>