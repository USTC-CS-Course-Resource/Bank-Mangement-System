<template>
  <card type="user">
    <div class="author">
      <div class="block block-one"></div>
      <div class="block block-two"></div>
      <div class="block block-three"></div>
      <div class="block block-four"></div>
      <a href="#">
        <img class="avatar" src="../../assets/img/anime3.png" alt="..." />
        <h5 class="title">{{ model.cus_name }}</h5>
      </a>
      <p class="description">
        {{ user.title }}
      </p>
    </div>
    <p class="card-description">phone: {{ model.cus_phone }}</p>
    <div slot="footer" class="button-container">
      <base-button icon round class="btn-facebook">
        <i class="fab fa-facebook"></i>
      </base-button>
      <base-button icon round class="btn-twitter">
        <i class="fab fa-twitter"></i>
      </base-button>
      <base-button icon round class="btn-google">
        <i class="fab fa-google-plus"></i>
      </base-button>
    </div>
  </card>
</template>
<script>
import { Card } from "@/components/index";

import BaseButton from "@/components/BaseButton";
import { eventBus } from "./eventbus";

export default {
  components: {
    Card,
    BaseButton
  },
  props: {
    user: {
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
      this.user.fullName = msg.cus_name;
      this.user.description = `${msg.cus_phone}`;
    });
  }
};
</script>
<style></style>
