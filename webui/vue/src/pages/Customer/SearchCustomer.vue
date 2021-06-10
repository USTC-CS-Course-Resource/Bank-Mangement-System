<template>
  <card>
    <template slot="header">
      <h5 class="title">Search Conditions</h5>
    </template>
    <div class="row">
      <div class="col-md-5 pr-md-1 text-left">
        <base-input
          label="Customer Id"
          placeholder="350581200001016666"
          v-model="model.cus_id"
        >
        </base-input>
      </div>
      <div class="col-md-3 px-md-1 text-left">
        <base-input
          label="Customer Name"
          placeholder="Jack"
          v-model="model.cus_name"
        >
        </base-input>
      </div>
      <div class="col-md-4 pl-md-1 text-left">
        <base-input
          label="Customer Phone"
          placeholder="+86 188 8888 8888"
          v-model="model.cus_phone"
        >
        </base-input>
      </div>
    </div>

    <div class="row">
      <div class="col-md-12 text-left">
        <base-input
          label="Customer Address"
          placeholder="USTC, Hefei, Anhui, China"
          v-model="model.cus_address"
        >
        </base-input>
      </div>
    </div>

    <div class="row">
      <div class="col-md-4 text-left">
        <base-input
          label="Contacts Name"
          placeholder="Jack"
          v-model="model.con_name"
        >
        </base-input>
      </div>
      <div class="col-md-4 pl-md-1 text-left">
        <base-input
          label="Contacts Phone"
          placeholder="+86 188 8888 8888"
          v-model="model.con_phone"
        >
        </base-input>
      </div>
      <div class="col-md-4 pl-md-1 text-left">
        <base-input
          label="Contacts Email"
          placeholder="+86 188 8888 8888"
          v-model="model.con_email"
        >
        </base-input>
      </div>
    </div>

    <div class="row">
      <div class="col-md-12 text-left">
        <base-input
          label="Relation between Customer and Contacts"
          placeholder="couple"
          v-model="model.con_relation"
        >
        </base-input>
      </div>
    </div>

    <template slot="footer">
      <base-button type="success" fill @click="submit">Search</base-button>
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
  data() {
    return {};
  },
  methods: {
    submit() {
      axios
        .post("http://localhost:5000/customer/search_customer", this.model)
        .then(response => {
          this.$notifyVue(
            `Search Customer: <b>${this.model.cus_name}</b>`,
            "top",
            "center",
            "success",
            2000
          );
          console.log("emit from search");
          this.$emit("returnResults", response.data);
        })
        .catch(() => {
          this.$notifyVue(`Search Failed!!`, "top", "center", "danger", 2000);
          this.$emit("returnResults", []);
        });
    }
  }
};
</script>
<style></style>
