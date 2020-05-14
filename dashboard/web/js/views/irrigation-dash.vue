<template>
  <v-card>
    <v-card-text>
      <apexchart type="area" :options="options" :series="series"></apexchart>
    </v-card-text>
  </v-card>
</template>
<script>
module.exports = {
  props: ["managementClient", "zone"],
  data: () => ({
    options: {
      chart: {
        height: 100,
        toolbar: {
          show: false
        }
      },
      title: {
        text: ""
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
        },
        tooltip: {
          formatter: (val, opts) => {
            return moment(val).format("MMM Do h:mm");
          }
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
      ],
      annotations: {
        yaxis: [
          {
            y: 0,
            label: {
              text: "Max water level"
            }
          }
        ]
      }
    },
    series: []
  }),
  created() {
    this.load();
  },
  methods: {
    load() {
      this.options.title.text = this.zone.name;
      this.options.annotations.yaxis[0].y = this.zone.maxWaterAmountMm;

      const request = new proto.ha.irrigation.GetWaterLevelHistoryRequest();
      request.setZoneId(this.zone.id);
      request.setMaxDays(3);
      this.managementClient.getWaterLevelHistory(
        request,
        {},
        (err, response) => {
          this.onLoad(response);
        }
      );
    },
    onLoad(response) {
      const waterLevels = response.getWaterLevelsList();
      this.series = [
        {
          name: this.zone.name,
          type: "area",
          data: waterLevels.map(x => [
            x.getTimeslot().toDate(),
            x.getCurrentAmountMm()
          ])
        }
      ];
    }
  }
};
</script>
<style scoped></style>
