<template>
  <card type="user">
    <div class="author">
      <div class="block block-one"></div>
      <div class="block block-two"></div>
      <div class="block block-three"></div>
      <div class="block block-four"></div>
      <a href="#">
        <h5 class="title">{{ model.bra_name }}</h5>
      </a>
      <p class="description">{{ card.title }} -- {{ model.acc_type }} type</p>
    </div>
    <p class="card-description">{{ card.description }}</p>
    <br />
    <p class="description">Account ID: {{ model.acc_id }}</p>
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
    card: {
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
    });
  }
};
</script>
<style></style>
