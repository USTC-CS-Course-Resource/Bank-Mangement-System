<template>
  <card>
    <template slot="header">
      <h5 class="title">Create Account</h5>
    </template>
    <div class="row">
      <div class="col-md-5 pr-md-1 text-left">
        <base-input
          label="Account Id"
          placeholder="Account Id"
          v-model="model.acc_id"
        >
        </base-input>
      </div>
    </div>
    <div class="row">
      <div class="col-md-5 pr-md-1 text-left">
        <base-input
          label="Customer Id"
          placeholder="Customer Id"
          v-model="model.cus_id"
        >
        </base-input>
      </div>
      <div class="col-md-5 px-md-1 text-left">
        <base-input
          label="Branch Name"
          placeholder="Branch Name"
          v-model="model.bra_name"
        >
        </base-input>
      </div>
      <div class="col-md-2 px-md-1 text-left">
        <base-input label="Account Type">
          <select
            id="inputAccountType"
            class="form-control"
            v-model="model.acc_type"
          >
            <option selected>STORE</option>
            <option>CHECK</option>
          </select>
        </base-input>
      </div>
    </div>
    <div class="row" v-if="model.acc_type == 'STORE'">
      <div class="col-md-6 pr-md-1 text-left">
        <base-input
          label="Interest Rate"
          placeholder="0.02"
          v-model="model.sto_interest_rate"
        >
        </base-input>
      </div>
      <div class="col-md-2 px-md-1 text-left">
        <base-input label="Currency Type">
          <select
            label="Currency Type"
            class="form-control"
            placeholder="CNY"
            v-model="model.sto_currency_type"
          >
            <option selected>CNY</option>
            <option>USD</option>
          </select>
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
import { eventBus } from "./eventbus";

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
        acc_type: this.model.acc_type,
        cus_name: this.model.cus_id,
        cus_id: this.model.cus_id,
        cus_phone: this.model.cus_phone
      };
    },
    acc_type_int: function() {
      if (this.model.acc_type == "STORE") return 0;
      else if (this.model.acc_type == "CHECK") return 1;
      else return -1;
    }
  },
  watch: {
    description: function() {
      console.log(`change! ${this.description}`);
      eventBus.$emit("description", this.description);
    }
  },
  methods: {
    create() {
      let data = { ...this.model };
      console.log(this.model.acc_type);
      data.acc_type = this.acc_type_int;
      console.log(this.model);
      console.log(data);
      axios
        .post("http://localhost:5000/account/open_account", {
          ...data,
          token: this.$store.state.token
        })
        .then(() => {
          this.$notifyVue(
            `Create <b>${this.model.acc_type} ACCOUNT</b> for <b>${data.cus_id}</b>`,
            "top",
            "center",
            "success",
            2000
          );
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
                `Creating Failed! (${error.response.data})`,
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
