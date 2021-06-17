<template>
  <card type="user">
    <div class="author">
      <div class="block block-one"></div>
      <div class="block block-two"></div>
      <div class="block block-three"></div>
      <div class="block block-four"></div>
      <a href="#">
        <img class="avatar" src="../../assets/img/anime3.png" alt="..." />
        <h4 class="title">{{ model.cus_name }}</h4>
      </a>
      <p class="description">
        {{ cus.title }}
      </p>
    </div>
    <p class="card-description">
      ID: {{ model.cus_id }} <br />
      Phone: {{ model.cus_phone }} <br />
      Address: {{ model.cus_address }} <br />
      Contacts Name: {{ model.con_name }} <br />
      Contacts Phone: {{ model.con_phone }} <br />
      Contacts Email: {{ model.con_email }} <br />
    </p>
  </card>
</template>
<script>
import { Card } from "@/components/index";

import { eventBus } from "./eventbus";

export default {
  components: {
    Card
  },
  props: {
    cus: {
      type: Object,
      default: () => {
        return {};
      }
    },
    model: {
      type: Object,
      default: () => {
        return {};
      }
    }
  },
  mounted() {
    eventBus.$on("description", msg => {
      console.log("get", msg);
      this.cus.fullName = msg.cus_name;
      this.cus.description = `${msg.cus_phone}`;
    });
  }
};
</script>
<style></style>
