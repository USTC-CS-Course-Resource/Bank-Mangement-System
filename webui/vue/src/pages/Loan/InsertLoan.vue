<template>
  <card>
    <template slot="header">
      <h5 class="title">Insert Loan</h5>
    </template>
    <div class="row">
      <div class="col-md-5 px-md-1 text-left">
        <base-input
          label="Branch Name"
          placeholder="憨憨银行合肥分行"
          v-model="model.bra_name"
        >
        </base-input>
      </div>
      <div class="col-md-5 pr-md-1 text-left">
        <base-input
          label="Loan Amount"
          type="Number"
          placeholder="0"
          v-model="model.loa_amount"
          required
        >
        </base-input>
      </div>
    </div>
    <div class="row">
      <div class="col-md-5 px-md-1 text-left">
        <base-input
          label="Customer ID"
          placeholder="350500200001011111"
          v-model="model.cus_ids[0]"
        >
        </base-input>
      </div>
    </div>
    <template slot="footer">
      <base-button type="success" fill @click="create">Create</base-button>
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
    model: {
      type: Object,
      default: () => {
        return {};
      }
    }
  },
  computed: {
    description() {
      return {
        cus_name: this.model.cus_id,
        cus_id: this.model.cus_id,
        cus_phone: this.model.cus_phone
      };
    },
    acc_type_int: function() {
      if (this.accountType == "STORE") return 0;
      else if (this.accountType == "CHECK") return 1;
      else return -1;
    }
  },
  methods: {
    create() {
      axios
        .post("http://localhost:5000/loan/insert_loan", this.model)
        .then(response => {
          console.log(response);
          this.$notifyVue(
            `Create a loan(<b>id=${response.data}</b>) of <b>${this.model.loa_amount}</b> for <b>${this.model.cus_ids}</b>`,
            "top",
            "center",
            "success",
            2000
          );
        })
        .catch(error => {
          this.$notifyVue(
            `Creating Failed! (${error.response.data})`,
            "top",
            "center",
            "danger",
            2000
          );
        });
    }
  }
};
</script>
<style></style>
