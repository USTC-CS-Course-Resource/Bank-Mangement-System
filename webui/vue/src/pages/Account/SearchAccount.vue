<template>
  <card>
    <template slot="header">
      <h5 class="title">Search Conditions</h5>
    </template>
    <div class="row">
      <div class="col-md-4 pr-md-1 text-left">
        <base-input
          label="Account ID"
          placeholder="Account ID(16 digits)"
          v-model="model.acc_id"
        >
        </base-input>
      </div>
      <div class="col-md-4 pr-md-1 text-left">
        <base-input
          label="Customer Id"
          placeholder="Customer Id(18 digits)"
          v-model="model.cus_id"
        >
        </base-input>
      </div>
      <div class="col-md-4 px-md-1 text-left">
        <base-input
          label="Branch Name"
          placeholder="Branch Name"
          v-model="model.bra_name"
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
      accountType: "STORE",
      model: {}
    };
  },
  watch: {
    shouldReSearch: function() {
      this.search();
    }
  },
  computed: {
    acc_type_int: function() {
      if (this.model.acc_type == "STORE") return 0;
      else if (this.model.acc_type == "CHECK") return 1;
      else return -1;
    }
  },
  methods: {
    search() {
      axios
        .post("http://localhost:5000/account/search_account", {
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
          }
        });
    }
  }
};
</script>
<style></style>
