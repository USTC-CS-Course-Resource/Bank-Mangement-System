<template>
  <div class="content">
    <card>
      <template slot="header">
        <h3 class="title">Login Before Continuing</h3>
      </template>
      <div class="row">
        <div class="col-md-5 pr-md-1 text-left">
          <base-input
            label="User Name"
            placeholder="User Name"
            v-model="username"
          >
          </base-input>
        </div>
      </div>
      <div class="row">
        <div class="col-md-3 pr-md-1 text-left">
          <base-input
            label="Password"
            placeholder="Password"
            v-model="password"
          >
          </base-input>
        </div>
      </div>

      <template slot="footer">
        <base-button type="success" fill @click="login">Login</base-button>
      </template>
    </card>
  </div>
</template>
<script>
import { Card, BaseInput } from "@/components/index";

import BaseButton from "@/components/BaseButton";
import axios from "axios";

export default {
  components: {
    Card,
    BaseInput,
    BaseButton
  },
  props: {
    query: {
      type: Object,
      default: () => {
        return {};
      }
    }
  },
  data() {
    return {
      username: null,
      password: null,
      token: null
    };
  },
  methods: {
    login() {
      axios
        .post("http://localhost:5000/login", {
          username: this.username,
          password: this.password
        })
        .then(response => {
          console.log(response.data);
          console.log(this.$route.query);
          if (response.data.status == "ok") {
            this.$store.state.username = response.data.username;
            this.$store.state.token = response.data.token;
            this.$notifyVue(
              `Welcome ${this.username}!`,
              "top",
              "center",
              "success",
              2000
            );
            console.log(`route to: ${this.$route.query.redirect}`);
            if (!this.$route.query.redirect) {
              this.$router.push({ path: "/dashboard" });
            } else {
              this.$router.push({ path: this.$route.query.redirect });
            }
          } else {
            this.$notifyVue(
              `Wrong Password or Username`,
              "top",
              "center",
              "danger",
              2000
            );
          }
        })
        .catch(error => {
          if (!error.response) {
            this.$notify_connection_error(error);
            return;
          }
          this.$notifyVue(
            `Login Failed! (${error.response.data})`,
            "top",
            "center",
            "danger",
            4000
          );
        });
    }
  }
};
</script>
<style></style>
