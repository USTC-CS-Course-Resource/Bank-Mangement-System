<template>
  <div class="content">
    <!--------------------------- Loan Customer Information Modal --------------------------->
    <div class="col-md-4">
      <modal :show.sync="modals.loanCustomerInfoModal">
        <template slot="header">
          <h5 class="modal-title">Loan Customer Information</h5>
        </template>
        <div>
          <div
            v-for="(item, index) in loanCustomerInfoModalTableData"
            :key="index"
          >
            <template
              v-for="(column, index) in loanCustomerInfoModalTableColumns"
            >
              <p :key="index" v-if="hasValue(item, column)">
                {{ itemValue(item, column) }}
              </p>
            </template>
          </div>
        </div>
        <template slot="footer">
          <base-button
            type="secondary"
            @click="modals.loanCustomerInfoModal = false"
            >Close</base-button
          >
        </template>
      </modal>
    </div>
    <!--------------------------------------------------------------------------------------->
    <div class="col-md-12">
      <a-tabs default-active-key="InsertTab" v-model="activeKey">
        <a-tab-pane key="InsertTab" tab="Insert Loan">
          <div class="row">
            <div class="col-md-12">
              <insert-loan :model="insertModel"> </insert-loan>
            </div>
          </div>
        </a-tab-pane>
        <a-tab-pane key="SearchTab" tab="Search Loan" force-render>
          <div class="row">
            <div class="col-md-12">
              <search-loan
                v-on:searchResultsTableHandle="searchResultsTableHandle"
                :shouldReSearch="shouldReSearch"
              >
              </search-loan>
            </div>
          </div>
          <div class="row">
            <div class="col-12">
              <card>
                <template slot="header">
                  <h4 class="card-title">Search Results</h4>
                </template>
                <div class="table-responsive text-left">
                  <search-results-table
                    v-on:searchResultsTableHandle="searchResultsTableHandle"
                    :data="tableData"
                    :columns="tableColumns"
                    thead-classes="text-primary"
                  >
                  </search-results-table>
                </div>
              </card>
            </div>
          </div>
        </a-tab-pane>
        <a-tab-pane key="PayLoanTab" tab="Pay Loan" disabled>
          <div class="row">
            <div class="col-md-12">
              <pay-loan
                :model="payLoanModel"
                v-on:searchResultsTableHandle="searchResultsTableHandle"
              >
              </pay-loan>
            </div>
          </div>
          <div class="row">
            <div class="col-12">
              <card>
                <template slot="header">
                  <h4 class="card-title">Pay Loan Records</h4>
                </template>
                <div class="table-responsive text-left">
                  <pay-loan-table
                    v-on:searchResultsTableHandle="searchResultsTableHandle"
                    :data="payLoanTableData"
                    :columns="payLoanTableColumns"
                    thead-classes="text-primary"
                  >
                  </pay-loan-table>
                </div>
              </card>
            </div>
          </div>
        </a-tab-pane>
      </a-tabs>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import { Card } from "@/components/index";
import BaseButton from "@/components/BaseButton";
import Modal from "@/components/Modal";
import InsertLoan from "./Loan/InsertLoan.vue";
import SearchLoan from "./Loan/SearchLoan.vue";
import PayLoan from "./Loan/PayLoan.vue";
import SearchResultsTable from "./Loan/SearchResultsTable.vue";
// import LoanCustomerInfoModalTable from "./Loan/LoanCustomerInfoModalTable.vue";
import PayLoanTable from "./Loan/PayLoanTable.vue";

export default {
  components: {
    Card,
    BaseButton,
    Modal,
    InsertLoan,
    SearchLoan,
    PayLoan,
    SearchResultsTable,
    // LoanCustomerInfoModalTable,
    PayLoanTable
  },
  data() {
    return {
      insertModel: {
        cus_ids: ["350500200001011111"],
        bra_name: "憨憨银行合肥分行"
      },
      payLoanModel: {
        payLoanRecords: [],
        loa_pay_amount_sum: 0
      },
      tableColumns: ["loa_id", "bra_name", "loa_amount", "actions"],
      tableData: [],
      payLoanTableColumns: ["loa_pay_id", "loa_pay_amount", "loa_pay_date"],
      payLoanTableData: [],
      loanCustomerInfoModalTableColumns: ["cus_id"],
      loanCustomerInfoModalTableData: [],
      modals: {
        loanCustomerInfoModal: false
      },
      loanModalData: {
        acc_id: "xxxxxxxxxxxxxxxx",
        acc_balance: 0
      },
      shouldReSearch: 0,
      activeKey: "SearchTab"
    };
  },
  computed: {
    isModalCHECK: function() {
      return this.loanModalData.acc_type == "CHECK";
    }
  },
  methods: {
    hasValue(item, column) {
      return item[column.toLowerCase()] !== "undefined";
    },
    itemValue(item, column) {
      column = column.toLowerCase();
      if (column == "loa_amount") {
        return this.$format_money(item[column]);
      }
      return item[column.toLowerCase()];
    },
    searchResultsTableHandle(event) {
      if (event.type == "updateResults") {
        console.log(event.data);
        this.tableData = event.data;
      } else if (event.type == "showPayRecords") {
        this.showPayRecords(event.data);
      } else if (event.type == "showCustomerInfo") {
        this.showCustomerInfo(event.data);
      }
    },
    showPayRecords(item) {
      axios
        .post("http://localhost:5000/loan/get_pay_loa_records", {
          ...item,
          token: this.$store.state.token
        })
        .then(response => {
          let data = response.data;
          this.payLoanModel = { ...data, ...item };
          console.log("showPayRecords");
          console.log(this.payLoanModel);
          this.payLoanTableData = response.data.payLoanRecords;
          this.activeKey = "PayLoanTab";
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
                `Get Details Failed! (${error.response.data})`,
                "top",
                "center",
                "danger",
                4000
              );
            }
          }
        });
    },
    showCustomerInfo(item) {
      axios
        .post("http://localhost:5000/loan/get_customer_info", {
          ...item,
          token: this.$store.state.token
        })
        .then(response => {
          this.loanCustomerInfoModalTableData = response.data;
          console.log("related customer info:");
          console.log(this.loanCustomerInfoModalTableData);
          this.modals.loanCustomerInfoModal = true;
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
                `Get Customer Information Failed! (${error.response.data})`,
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
