<template>
  <v-card>
    <v-card-text>
      <apexchart type="area" :options="options" :series="series"></apexchart>
    </v-card-text>
  </v-card>
</template>
<script>
module.exports = {
  props: ["weatherService"],
  data: () => ({
    options: {
      chart: {
        height: 100,
        toolbar: {
          show: false
        }
      },
      title: {
        text: "Rain"
      },
      dataLabels: {
        enabled: false
      },
      markers: {
        size: 0
      },
      xaxis: {
        type: "datetime",
        labels: {
          format: "MM/dd HH:mm"
        }
      },
      yaxis: [
        {
          title: {
            text: "Amount (mm)"
          },
          labels: {
            formatter(val) {
              return val.toFixed(2);
            }
          }
        }
      ]
    },
    series: []
  }),
  created() {
    this.load();
  },
  methods: {
    load() {
      const request = new proto.ha.weather.GetSnapshotsRequest();
      request.setZipcode("98004");
      request.setMaxDays(3);
      this.weatherService.getSnapshots(request, {}, (err, response) => {
        this.onLoad(response);
      });
    },
    onLoad(response) {
      const snapshots = response.getSnapshotsList();
      this.series = [
        {
          name: "Rain",
          type: "area",
          data: snapshots.map(x => [
            x.getTimestamp().toDate(),
            x.getLast1HourRainAmountMm()
          ])
        }
      ];
    }
  }
};
</script>
<style scoped>
</style>
