const ROUTES = [
  {
    path: "/",
    redirect: "/security",
  },
  {
    path: "/security",
    component: httpVueLoader("js/views/security.vue"),
  },
  {
    path: "/irrigation",
    component: httpVueLoader("js/views/irrigation.vue"),
  },
  {
    path: "/gallery",
    component: httpVueLoader("js/views/gallery.vue"),
  },
];
