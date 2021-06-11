<template>
  <div class="col-md-8">
    <modal
      :show.sync="localStoreAccountModal"
      body-classes="p-0"
      modal-classes="modal-dialog-centered modal-sm"
    >
      <card
        type="secondary"
        header-classes="bg-white pb-5"
        body-classes="px-lg-5 py-lg-5"
        class="border-0 mb-0"
      >
        <template>
          <div class="text-muted text-center mb-3">
            <small>Sign in with</small>
          </div>
          <div class="btn-wrapper text-center">
            <base-button type="default">
              <img
                slot="icon"
                src="https://demos.creative-tim.com/argon-design-system/assets/img/icons/common/github.svg"
              />
              Github
            </base-button>

            <base-button type="danger">
              <img
                slot="icon"
                src="https://demos.creative-tim.com/argon-design-system/assets/img/icons/common/google.svg"
              />
              Google
            </base-button>
          </div>
        </template>
        <template>
          <div class="text-center text-muted mb-4">
            <small>Or sign in with credentials</small>
          </div>
          <form role="form">
            <base-input
              alternative
              class="mb-3"
              placeholder="Email"
              addon-left-icon="tim-icons icon-single-02"
            >
            </base-input>
            <base-input
              alternative
              type="password"
              placeholder="Password"
              addon-left-icon="tim-icons icon-lock-circle"
            >
            </base-input>
            <base-checkbox>
              Remember me
            </base-checkbox>
            <div class="text-center">
              <base-button type="primary" class="my-4">Sign In</base-button>
            </div>
          </form>
        </template>
      </card>
    </modal>
  </div>
</template>

<script>
import { Card, BaseInput } from "@/components/index";
import BaseButton from "@/components/BaseButton";
import Modal from "@/components/Modal";

export default {
  name: "store-account-modal",
  components: {
    Card,
    BaseInput,
    BaseButton,
    Modal
  },
  props: {
    storeAccountModal: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      localStoreAccountModal: false
    };
  },
  watch: {
    storeAccountModal() {
      console.log("fuckit");
      this.localStoreAccountModal = this.storeAccountModal;
    }
  }
};
</script>
<style></style>
