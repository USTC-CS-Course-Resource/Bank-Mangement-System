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
      <tr v-for="(item, index) in data" :key="index">
        <slot :row="item">
          <template v-for="(column, index) in columns">
            <td :key="index" v-if="hasValue(item, column)">
              {{ itemValue(item, column) }}
            </td>
          </template>
          <!-- operation buttons -->
          <td class="td-actions text-right">
            <base-button
              type="success"
              size="sm"
              icon
              @click="editCustomer(item)"
            >
              <i class="tim-icons icon-settings"></i>
            </base-button>
            <base-button
              type="danger"
              size="sm"
              icon
              @click="removeCustomer(item, index)"
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
    removeCustomer(item, index) {
      console.log(this.data);
      console.log(item);
      axios
        .post("http://localhost:5000/customer/remove_customer", {
          ...item,
          token: this.$store.state.token
        })
        .then(() => {
          this.$notifyVue(
            `Remove Customer: <b>${item.cus_name}</b>`,
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
            this.$emit("searchResultsTableHandle", {
              data: [],
              type: "updateResults"
            });
          }
        });
    },
    editCustomer(item) {
      console.log("in");
      console.log(item);
      this.$emit("searchResultsTableHandle", {
        data: item,
        type: "updateCustomer"
      });
    }
  }
};
</script>
<style></style>
