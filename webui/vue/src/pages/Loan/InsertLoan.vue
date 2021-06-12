<template>
  <card>
    <template slot="header">
      <h5 class="title">Insert Loan</h5>
    </template>
    <div class="row">
      <div class="col-md-5 text-left">
        <base-input
          label="Branch Name"
          placeholder="憨憨银行合肥分行"
          v-model="local_model.bra_name"
        >
        </base-input>
      </div>
    </div>
    <div class="row">
      <div class="col-md-5 text-left">
        <base-input
          label="Loan Amount"
          type="Number"
          placeholder="0"
          v-model="local_model.loa_amount"
          required
        >
        </base-input>
      </div>
      <div class="col-md-5 text-left">
        <base-input
          label="Formatted Loan Amount"
          type="String"
          placeholder="0.00"
          v-model="format_loa_amount"
          required
        >
        </base-input>
      </div>
    </div>
    <div class="row">
      <div class="col-md-5 text-left">
        <div class="grow-wrap">
          <base-textarea
            label="Customer ID"
            placeholder="350500200001011111"
            v-model="cus_ids_text"
          >
          </base-textarea>
        </div>
      </div>
    </div>
    <template slot="footer">
      <base-button type="success" fill @click="create">Create</base-button>
    </template>
  </card>
</template>
<script>
import { Card, BaseInput, BaseTextarea } from "@/components/index";

import BaseButton from "@/components/BaseButton";
import axios from "axios";

export default {
  components: {
    Card,
    BaseInput,
    BaseButton,
    BaseTextarea
  },
  props: {
    model: {
      type: Object,
      default: () => {
        return {};
      }
    }
  },
  data() {
    return {
      local_model: {
        bra_name: "憨憨银行合肥分行",
        loa_amount: 0,
        cus_ids: ["350500200001011111"]
      },
      cus_ids_text: "350500200001011111"
    };
  },
  watch: {
    model: function() {
      this.local_model = this.model;
    },
    cus_ids: function() {
      this.local_model.cus_ids = this.cus_ids;
    }
  },
  computed: {
    format_loa_amount: function() {
      return this.$format_money(this.local_model.loa_amount);
    },
    cus_ids: function() {
      return this.cus_ids_text
        .split("\n")
        .map(e => e.replace(/^[\t\r\n ]*|[\t\r\n ]*$/g, ""));
    }
  },
  methods: {
    create() {
      axios
        .post("http://localhost:5000/loan/insert_loan", this.local_model)
        .then(response => {
          console.log(response);
          this.$notifyVue(
            `Create a loan(<b>id=${response.data}</b>) of <b>${this.local_model.loa_amount}</b> for <b>${this.local_model.cus_ids}</b>`,
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
