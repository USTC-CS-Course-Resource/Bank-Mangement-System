<template>
  <card>
    <template slot="header">
      <h5 class="title">Search Conditions</h5>
    </template>
    <div class="row">
      <div class="col-md-5 text-left">
        <base-input
          label="Branch Name"
          placeholder="Branch Name"
          v-model="model.bra_name"
        >
        </base-input>
      </div>
      <div class="col-md-5 text-left">
        <base-input
          label="Loan ID"
          type="Number"
          placeholder="Loan ID"
          v-model="model.loa_id"
          required
        >
        </base-input>
      </div>
    </div>
    <div class="row">
      <div class="col-md-5 text-left">
        <base-input
          label="Customer ID"
          placeholder="Customer ID"
          v-model="model.cus_id"
        >
        </base-input>
      </div>
    </div>
    <template slot="footer">
      <base-button type="success" fill @click="search">Search</base-button>
    </template>
  </card>
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
    shouldReSearch: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      model: {}
    };
  },
  watch: {
    shouldReSearch: function() {
      this.search();
    }
  },
  methods: {
    search() {
      axios
        .post("http://localhost:5000/loan/search_loan", {
          ...this.model,
          token: this.$store.state.token
        })
        .then(response => {
          console.log(response);
          this.$notifyVue(`Search Succeed!`, "top", "center", "success", 2000);
          console.log(response.data);
          this.$emit("searchResultsTableHandle", {
            data: response.data,
            type: "updateResults"
          });
        })
        .catch(error => {
          if (!error.response) {
            this.$notify_connection_error(error);
          } else {
            console.log(error.response);
            if (
              error.response.data == "LoginExpired" ||
              error.response.data.includes("ExpiredSignatureError")
            ) {
              this.$loginExpiredAction();
            } else {
              this.$notifyVue(
                `Search Failed! (${error.response.data})`,
                "top",
                "center",
                "danger",
                4000
              );
            }
            this.$emit("searchResultsTableHandle", {
              data: [],
              type: "updateResults"
            });
          }
        });
    }
  }
};
</script>
<style></style>
