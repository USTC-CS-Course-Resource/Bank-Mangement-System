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
        </slot>
      </tr>
    </tbody>
  </table>
</template>
<script>
import axios from "axios";

export default {
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
      column = column.toLowerCase();
      if (column == "loa_pay_amount") {
        return this.$format_money(item[column]);
      }
      return item[column.toLowerCase()];
    },
    removeLoan(item, index) {
      axios
        .post("http://localhost:5000/loan/remove_loan", {
          ...item,
          token: this.$store.state.token
        })
        .then(() => {
          this.$notifyVue(
            `Remove Loan: <b>${item.loa_id}</b>`,
            "top",
            "center",
            "success",
            2000
          );
          this.data.splice(index, 1);
          this.$emit("searchResultsTableHandle", {
            data: this.data,
            type: "updateResults"
          });
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
                `Removing Failed! (${error.response.data})`,
                "top",
                "center",
                "danger",
                4000
              );
            }
          }
        });
    },
    showStoreAccountModal(item, index) {
      this.$emit("searchResultsTableHandle", {
        type: "showStoreAccountModal",
        data: { ...item, index: index }
      });
    },
    showPayRecords(item) {
      this.$emit("searchResultsTableHandle", {
        type: "showPayRecords",
        data: item
      });
    }
  }
};
</script>
<style></style>
