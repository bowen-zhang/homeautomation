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
  data() {
    return {
      options: {
        xaxis: {
          type: "datetime"
        },
        yaxis: [
          {
            min: 0
          }
        ]
      },
      series: []
    };
  },
  watch: {
    zone: {
      handler(newVal) {
        if (newVal) {
          this.refresh();
        }
      },
      immediate: true
    }
  },
  methods: {
    refresh() {
      const request = new proto.ha.irrigation.GetWaterLevelHistoryRequest();
      request.setZoneId(this.zone.id);
      request.setMaxDays(3);
      this.managementClient.getWaterLevelHistory(
        request,
        {},
        (err, response) => {
          this.onRefresh(response);
        }
      );
    },
    onRefresh(response) {
      const waterLevels = response.getWaterLevelsList();
      this.options = this.getOptions(response);
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
    },
    getOptions(response) {
      const runs = response.getRunsList();
      const options = {
        chart: {
          height: 200,
          toolbar: {
            show: false
          }
        },
        title: {
          text: this.zone.name
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
            min: 0,
            max: max => {
              return Math.ceil(Math.max(max, this.zone.maxWaterAmountMm));
            },
            tickAmount: 10,
            title: {
              text: "Amount (mm)"
            },
            labels: {
              formatter(val) {
                return val.toFixed(1);
              }
            }
          }
        ],
        annotations: {
          yaxis: [
            {
              y: this.zone.maxWaterAmountMm,
              label: {
                text: "Max water level"
              }
            }
          ]
        }
      };
      options.annotations.xaxis = runs.map(run => ({
        x: run
          .getStartAt()
          .toDate()
          .getTime(),
        x2: run
          .getStopAt()
          .toDate()
          .getTime(),
        fillColor: "#B3F7CA",
        label: {
          text: "Irrigation",
          position: "bottom",
          offsetY: 20
        }
      }));
      return options;
    }
  }
};
</script>
<style scoped></style>
