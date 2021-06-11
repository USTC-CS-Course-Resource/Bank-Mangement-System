<template>
  <card>
    <template slot="header">
      <h5 class="title">Search Conditions</h5>
    </template>
    <div class="row">
      <div class="col-md-4 pr-md-1 text-left">
        <base-input
          label="Account ID"
          placeholder="0000000000000000"
          v-model="model.acc_id"
        >
        </base-input>
      </div>
      <div class="col-md-4 pr-md-1 text-left">
        <base-input
          label="Customer Id"
          placeholder="350581200001016666"
          v-model="model.cus_id"
        >
        </base-input>
      </div>
      <div class="col-md-4 px-md-1 text-left">
        <base-input
          label="Branch Name"
          placeholder="憨憨银行合肥分行"
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
      modals: {
        checkAccountModal: false,
        storeAccountModal: false,
        modal1: false
      },
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
        .post("http://localhost:5000/account/search_account", this.model)
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
          this.$notifyVue(
            `Search Failed! (${error.response.data})`,
            "top",
            "center",
            "danger",
            2000
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
