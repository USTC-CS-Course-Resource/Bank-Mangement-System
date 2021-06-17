import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const state = {
  username: null,
  token: null
};

export default new Vuex.Store({
  state
});
