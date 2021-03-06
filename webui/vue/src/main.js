/*!

=========================================================
* Vue White Dashboard - v1.0.0
=========================================================

* Product Page: https://www.creative-tim.com/product/vue-white-dashboard
* Copyright 2019 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/vue-white-dashboard/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import Vue from "vue";
import VueRouter from "vue-router";
import store from "./vuex/store";
import SocialSharing from "vue-social-sharing";
import VueGitHubButtons from "vue-github-buttons";
import "vue-github-buttons/dist/vue-github-buttons.css";
import App from "./App.vue";
import "@/assets/scss/white-dashboard.scss";
import "@/assets/css/nucleo-icons.css";
import "@/assets/demo/demo.css";
import Antd from "ant-design-vue";
import "ant-design-vue/dist/antd.css";
import axios from "axios";

import GlobalComponents from "./globalComponents";
import GlobalDirectives from "./globalDirectives";
import RTLPlugin from "./RTLPlugin";
import Notify from "@/components/NotificationPlugin";
import i18n from "./i18n";
import SideBar from "@/components/SidebarPlugin";

Vue.config.productionTip = false;

// router setup
import routes from "./router";

// configure router
const router = new VueRouter({
  routes, // short for routes: routes
  linkExactActiveClass: "active"
});

Vue.use(VueRouter);
Vue.use(SocialSharing);
Vue.use(VueGitHubButtons, { useCache: true });
Vue.use(GlobalComponents);
Vue.use(GlobalDirectives);
Vue.use(RTLPlugin);
Vue.use(SideBar);
Vue.use(Notify);
Vue.use(Antd);

Vue.prototype.$format_money = function(s) {
  s = String(s);
  if (/[^0-9.]/.test(s)) return "NaN";
  s = s.replace(/^(\d*)$/, "$1.");
  s = (s + "00").replace(/(\d*\.\d\d)\d*/, "$1");
  s = s.replace(".", ",");
  var re = /(\d)(\d{3},)/;
  while (re.test(s)) s = s.replace(re, "$1,$2");
  s = s.replace(/,(\d\d)$/, ".$1");
  s = s.replace(/^\./, "0.");
  return s;
};

Vue.prototype.$notify_connection_error = function(error) {
  console.log(error);
  this.$notifyVue(
    `Connecting Failed, please Check Back-end Server! (net::ERR_CONNECTION_REFUSED)`,
    "top",
    "center",
    "danger",
    2000
  );
};

Vue.prototype.$loginExpiredAction = function() {
  this.$router.push({ path: "/login" });
  Vue.prototype.$notifyVue(`Login Expired`, "top", "center", "danger", 2000);
};

Vue.prototype.$loginVerify = function() {
  axios
    .post("http://localhost:5000/login", {
      token: store.state.token
    })
    .then(response => {
      console.log(`response.data.status: ${response.data.status}`);
      if (response.data.status == "ok") {
        console.log("verified");
      } else {
        store.state.token = null;
        store.state.username = null;
        this.$router.push({ path: "/login" });
        Vue.prototype.$notifyVue(
          `Login Expired`,
          "top",
          "center",
          "danger",
          2000
        );
      }
    })
    .catch(error => {
      store.state.token = null;
      store.state.username = null;
      console.log(error);
      Vue.prototype.$notifyVue(`Please Login`, "top", "center", "danger", 2000);
      this.$router.push({ path: "/login" });
    });
};

router.beforeEach((to, from, next) => {
  console.log("beforeEach");
  console.log(to);
  console.log(from);
  console.log(store.state);
  if (to.meta.requireAuth) {
    axios
      .post("http://localhost:5000/login", {
        token: store.state.token
      })
      .then(response => {
        console.log(`response.data.status: ${response.data.status}`);
        if (response.data.status == "ok") {
          console.log("verified");
          next();
        } else {
          store.state.token = null;
          store.state.username = null;
          next({ path: "/login", query: { redirect: to.fullPath } });
          Vue.prototype.$notifyVue(
            `Please Login`,
            "top",
            "center",
            "danger",
            2000
          );
        }
      })
      .catch(error => {
        store.state.token = null;
        store.state.username = null;
        console.log(error);
        next({ path: "/login", query: { redirect: to.fullPath } });
      });
  } else {
    next();
  }
});

new Vue({
  router,
  i18n,
  store,
  render: h => h(App)
}).$mount("#app");
