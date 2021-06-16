<template>
  <card>
    <template slot="header">
      <h5 class="title">Search Conditions</h5>
    </template>
    <div class="row">
      <div class="col-md-5 pr-md-1 text-left">
        <base-input
          label="Customer Id"
          placeholder="Customer Id"
          v-model="model.cus_id"
        >
        </base-input>
      </div>
      <div class="col-md-3 px-md-1 text-left">
        <base-input
          label="Customer Name"
          placeholder="Customer Name"
          v-model="model.cus_name"
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
  data() {
    return {
      model: {
        cus_id: "350500200001011111",
        cus_name: "小憨憨"
      }
    };
  },
  methods: {
    search() {
      axios
        .post("http://localhost:5000/customer/search_customer", this.model)
        .then(response => {
          this.$notifyVue(
            `Search Customer: <br />` +
              `<b>cus_name</b>: ${this.model.cus_name}<br />` +
              `<b>cus_id</b>: ${this.model.cus_id}<br />` +
              `<b>#entities</b>: ${response.data.length}`,
            "top",
            "center",
            "success",
            2000
          );
          console.log("emit from search");
          console.log(this.model);
          this.$emit("searchResultsTableHandle", {
            data: response.data,
            type: "updateResults"
          });
        })
        .catch(error => {
          if (!error.response) {
            this.$notify_connection_error(error);
            return;
          }
          this.$notifyVue(
            `Search Failed! (${error.response.data})`,
            "top",
            "center",
            "danger",
            4000
          );
          this.$emit("searchResultsTableHandle", {
            data: [],
            type: "updateResults"
          });
        });
    }
  }
};
</script>
<style></style>
