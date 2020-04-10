Vue.directive("bubble", (el, binding, vnode) => {
  Object.keys(binding.modifiers).forEach((event) => {
    // Bubble events of Vue components
    if (vnode.componentInstance) {
      vnode.componentInstance.$on(event, (...args) => {
        vnode.context.$emit(event, ...args);
      });

      // Bubble events of native DOM elements
    } else {
      el.addEventListener(event, (payload) => {
        vnode.context.$emit(event, payload);
      });
    }
  });
});

function formatDate(value) {
  if (value) {
    return moment(value).format("MMM Do, YYYY");
  } else {
    return "";
  }
}

function formatPercentage(value) {
  if (value === undefined || isNaN(value)) {
    return "-";
  }
  value *= 100;
  if (value < -10 || value > 10) {
    return value.toFixed(0) + "%";
  } else {
    return value.toFixed(1) + "%";
  }
}

Vue.filter("date", formatDate);
Vue.filter("percentage", formatPercentage);

new Vue({
  el: "#app",
  data: {
    api: new Api(),
  },
  vuetify: new Vuetify(),
  router: new VueRouter({
    routes: ROUTES,
  }),
  components: {},
  created: function () {},
  methods: {},
});
