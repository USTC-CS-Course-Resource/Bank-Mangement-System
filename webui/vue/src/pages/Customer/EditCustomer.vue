<template>
  <card>
    <template slot="header">
      <h5 class="title">Add/Edit Profile</h5>
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
      <base-button type="success" fill @click="submit">Save</base-button>
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
  methods: {
    submit() {
      axios
        .post("http://localhost:5000/customer/insert_customer", this.model)
        .then(() => {
          this.$notifyVue(
            `Inserted Customer: <b>${this.model.cus_name}</b>`,
            "top",
            "center",
            "success",
            2000
          );
        })
        .catch(() => {
          this.$notifyVue(`Inserted Failed!!`, "top", "center", "danger", 2000);
        });
    }
  },
  computed: {
    description() {
      return {
        cus_name: this.model.cus_name,
        cus_id: this.model.cus_id,
        cus_phone: this.model.cus_phone
      };
    }
  },
  watch: {
    description: function() {
      console.log(`change! ${this.description}`);
      eventBus.$emit("description", this.description);
    }
  }
};
</script>
<style></style>
