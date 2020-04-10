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
    path: "/gallery",
    component: httpVueLoader("js/views/gallery.vue"),
  },
];
