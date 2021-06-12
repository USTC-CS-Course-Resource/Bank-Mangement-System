<template>
  <card>
    <template slot="header">
      <h5 class="title">Loan Information</h5>
    </template>
    <div class="row">
      <div class="col-md-5 text-left">
        <base-input
          label="Loan ID"
          type="Number"
          placeholder="0"
          v-model="model.loa_id"
          disabled
        >
        </base-input>
      </div>
      <div class="col-md-5 text-left">
        <base-input
          label="Branch Name"
          placeholder="憨憨银行合肥分行"
          v-model="model.bra_name"
          disabled
        >
        </base-input>
      </div>
    </div>
    <div class="row">
      <div class="col-md-5 text-left">
        <base-input
          label="Loan Amount"
          type="String"
          placeholder="0.00"
          v-model="format_loa_amount"
          disabled
        >
        </base-input>
      </div>
      <div class="col-md-5 text-left">
        <base-input
          label="Loan Pay Amount Sum"
          type="String"
          placeholder="0.00"
          v-model="format_loa_pay_amount_sum"
          disabled
        >
        </base-input>
      </div>
    </div>
    <card>
      <div class="row">
        <div class="col-md-5 text-left">
          <base-input
            label="Pay Loan Amount"
            type="Number"
            placeholder="0.00"
            v-model="model.loa_pay_amount"
          >
          </base-input>
        </div>
        <div class="col-md-5 text-left">
          <base-input
            label="Formatted Pay Loan Amount"
            type="String"
            placeholder="0.00"
            v-model="format_loa_pay_amount"
            disabled
          >
          </base-input>
        </div>
      </div>
    </card>
    <template slot="footer">
      <base-button type="success" fill @click="payLoan">Pay</base-button>
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
    },
    model: {
      type: Object,
      default: function() {
        return {};
      }
    }
  },
  computed: {
    format_loa_pay_amount_sum: function() {
      return this.$format_money(this.model.loa_pay_amount_sum);
    },
    format_loa_amount: function() {
      return this.$format_money(this.model.loa_amount);
    },
    format_loa_pay_amount: function() {
      return this.$format_money(this.model.loa_pay_amount);
    }
  },
  watch: {
    shouldReSearch: function() {
      this.search();
    }
  },
  methods: {
    search() {
      axios
        .post("http://localhost:5000/loan/search_loan", this.model)
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
    },
    payLoan() {
      console.log(this.model);
      this.model.loa_pay_amount = Number(this.model.loa_pay_amount);
      axios
        .post("http://localhost:5000/loan/pay_loan", this.model)
        .then(response => {
          console.log(response);
          this.$notifyVue(`Search Succeed!`, "top", "center", "success", 2000);
          console.log(response.data);
          this.$emit("searchResultsTableHandle", {
            data: this.model,
            type: "showPayRecords"
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
            data: this.model,
            type: "showPayRecords"
          });
        });
    }
  }
};
</script>
<style></style>
