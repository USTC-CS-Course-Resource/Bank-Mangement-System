<template>
  <table class="table tablesorter" :class="tableClass">
    <thead :class="theadClasses">
      <tr>
        <slot name="columns">
          <th v-for="column in columns" :key="column">{{ column }}</th>
        </slot>
      </tr>
    </thead>
    <tbody :class="tbodyClasses">
      <!-- <store-account-modal :modals="modals"> </store-account-modal> -->
      <tr v-for="(item, index) in data" :key="index">
        <slot :row="item">
          <template v-for="(column, index) in columns">
            <td :key="index" v-if="hasValue(item, column)">
              {{ itemValue(item, column) }}
            </td>
          </template>
          <!-- operation buttons -->
          <td class="td-actions text-right">
            <!-- update balance button -->
            <base-button
              type="success"
              size="sm"
              icon
              @click="showStoreAccountModal(item, index)"
            >
              <i class="tim-icons icon-pencil"></i>
            </base-button>
            <!-- edit button -->
            <base-button
              type="success"
              size="sm"
              icon
              @click="editAccount(item)"
            >
              <i class="tim-icons icon-settings"></i>
            </base-button>
            <!-- remove button -->
            <base-button
              type="danger"
              size="sm"
              icon
              @click="removeHaveAccount(item, index)"
            >
              <i class="tim-icons icon-simple-remove"></i>
            </base-button>
          </td>
        </slot>
      </tr>
    </tbody>
  </table>
</template>
<script>
import axios from "axios";
import BaseButton from "@/components/BaseButton";

export default {
  name: "search-results-table",
  components: {
    BaseButton
  },
  data() {
    return {
      modals: {
        checkAccountModal: false,
        storeAccountModal: false,
        modal1: false,
        modal0: false,
        modal3: false
      }
    };
  },
  props: {
    tableClass: {
      type: String,
      default: ""
    },
    theadClasses: {
      type: String,
      default: ""
    },
    tbodyClasses: {
      type: String,
      default: ""
    },
    data: {
      type: Array,
      default: () => []
    },
    columns: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    hasValue(item, column) {
      return item[column.toLowerCase()] !== "undefined";
    },
    itemValue(item, column) {
      return item[column.toLowerCase()];
    },
    removeHaveAccount(item, index) {
      axios
        .post("http://localhost:5000/account/remove_have_account", item)
        .then(() => {
          this.$notifyVue(
            `Remove Account: <b>${item.acc_id}</b>`,
            "top",
            "center",
            "success",
            2000
          );
          this.data.splice(index, 1);
          if (this.data[0].acc_type == "STORE") {
            this.$emit("searchResultsTableHandle", {
              data: { STORE: this.data },
              type: "updateStoreResults"
            });
          } else if (this.data[0].acc_type == "CHECK") {
            this.$emit("searchResultsTableHandle", {
              data: { CHECK: this.data },
              type: "updateCheckResults"
            });
          }
        })
        .catch(error => {
          this.$notifyVue(
            `Removing Failed! (${error.response.data})`,
            "top",
            "center",
            "danger",
            2000
          );
        });
    },
    showStoreAccountModal(item, index) {
      this.$emit("searchResultsTableHandle", {
        type: "showStoreAccountModal",
        data: { ...item, index: index }
      });
    }
  }
};
</script>
<style></style>
